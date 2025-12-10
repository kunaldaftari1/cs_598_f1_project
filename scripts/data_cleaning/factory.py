import requests
from datetime import datetime
import pandas as pd
import time

BASE = "https://api.openf1.org/v1"
ROWS = 25

# globals
session_df = None
sessions = []
race_result_df = None
circuits_df = None

def update_rows(num: int):
    global ROWS
    ROWS = num

def get_races_api(year: int, date):
    sessions = requests.get(f"{BASE}/sessions", params = {"year": year, "date_start>": date}).json()

    return sessions

def get_races(save = True, date_start = "2023-03-03", verbose = True):
    global session_df
    global sessions

    try:
        # Sessions Schema
        years = [2023, 2024, 2025] # 2023 is the earliest available in the API
        sessions = []

        for year in years:
            sessions.extend(get_races_api(year, date=date_start))

        # Construct Sessions Table
        session_df = pd.DataFrame(sessions)

        # drop unncessary columns: meeting_key, location, country_key, country_code, country_name, circuit_short_name, gmt_offset
        session_df = session_df.drop(columns=["meeting_key", "location", "country_key", "country_code", "country_name", "circuit_short_name", "gmt_offset"])

        # reorder columns to match schema: session_key, session_type, session_name, circuit_key, date_start, date_end, year
        session_df = session_df[["session_key", "session_type", "session_name", "circuit_key", "date_start", "date_end", "year"]]

        # check for missing values
        if verbose:
            print("Missing values:")
            print(session_df.isnull().sum())
            print(session_df.head(ROWS))
            

        # save to csv
        if save:
            session_df.to_csv("../../data/cleaned/sessions.csv", index=False)
            return "Success - Data Saved to data/cleaned/sessions.csv"

        return "Success - Data Not Saved"
    except Exception:
        return "Failed - Rate Limited"




def get_starting_grid_api(session_key: int, position: int):
    # sample curl "https://api.openf1.org/v1/starting_grid?session_key=7783&position%3C=3"
    # sample url: https://api.openf1.org/v1/starting_grid?session_key=7783&position<=3
    grid = requests.get(f"{BASE}/starting_grid", params = {"session_key": session_key, "position<": position}).json()

    return grid

def get_starting_grid(save = True):
    try:
        if session_df is None or session_df.empty:
            res = get_races(save=save, verbose=False)
            print(f"From get_races subcall: {res}")
            if "Failed" in res:
                return res

        # Starting Grid Schema
        starting_grids = []
        position = 20

        for session_key in session_df["session_key"]:
            # starting grid only exists for qualifying sessions
            if session_df.loc[session_df["session_key"] == session_key, "session_type"].values[0] == "Qualifying":
                starting_grids.extend(get_starting_grid_api(session_key, position = position))

                # add sleep to avoid rate limiting
                time.sleep(1)
        
        # Construct Starting Grid Table
        grid_df = pd.DataFrame(starting_grids)

        # drop unnecessary columns: meeting_key
        grid_df = grid_df.drop(columns=["meeting_key"])

        # reorder columns to match schema: session_key, driver_number, position, lap_duration
        grid_df = grid_df[["session_key", "driver_number", "position", "lap_duration"]]

        # check for missing values
        print(grid_df.isnull().sum())
        print(grid_df.head(ROWS))


        # lap_duration can be null for drivers who DNF, DNS, or DSQ prior to finishing the first lap
        # for now, we will keep it as null as we want to be able to distinguish between the slowest drivers
        # and those who did not finish the session

        # save to csv
        if save:
            grid_df.to_csv("../../data/cleaned/starting_grid.csv", index=False)
            return "Success - Data Saved to data/cleaned/starting_grid.csv"

        return "Success - Data Not Saved"
    except Exception:
        return "Failed - Rate Limited"


def get_race_result_api(session_key: int, position: int):
    # sample curl "https://api.openf1.org/v1/session_result?session_key=7782&position%3C=3"
    # sample url: https://api.openf1.org/v1/session_result?session_key=7782&position<=3
    result = requests.get(f"{BASE}/session_result", params = {"session_key": session_key, "position<": position}).json()

    return result

def get_race_result(save = True, verbose = True):
    try:
        global race_result_df
        if session_df is None or session_df.empty:
            res = get_races(save=save, verbose=False)
            print(f"From get_races subcall: {res}")
            if "Failed" in res:
                return res            
        # Race Result Schema
        race_results = []
        position = 20

        for session_key in session_df["session_key"]:
            if session_df.loc[session_df["session_key"] == session_key, "session_type"].values[0] == "Race":
                race_results.extend(get_race_result_api(session_key, position = position))

                # add sleep to avoid rate limiting
                time.sleep(1)

        # Construct Race Result Table
        race_result_df = pd.DataFrame(race_results)

        # drop unnecessary columns: meeting_key, points, duration, gap_to_leader, 
        race_result_df.drop(columns=["meeting_key", "points", "duration", "gap_to_leader", "number_of_laps"], inplace=True)

        # go through dnf, dns and dsq, if one is true, set driver_status to the first one that is true, if none are true, set to finished
        def determine_driver_status(row):
            if row.get('dnf', False):
                return "dnf"
            elif row.get('dns', False):
                return "dns"
            elif row.get('dsq', False):
                return "dsq"
            else:
                return "finished"

        race_result_df['driver_status'] = race_result_df.apply(determine_driver_status, axis=1)

        # we no longer need the dnf, dns and dsq columns
        race_result_df.drop(columns=["dnf", "dns", "dsq"], inplace=True)

        # reorder columns to match schema: session_key, driver_number, position, driver_status
        race_result_df = race_result_df[["session_key", "driver_number", "position", "driver_status"]]

        # check for missing values
        if verbose:
            print(race_result_df.isnull().sum())
            print(race_result_df.head(ROWS)) 

        # save to csv
        if save:
            race_result_df.to_csv("../../data/cleaned/race_result.csv", index=False)
            return "Success - Data Saved to data/cleaned/race_result.csv"

        return "Success - Data Not Saved"
    except Exception:
        return "Failed - Rate Limited"

def get_circuits(save = True, verbose = True):
    global circuits_df

    try:
        # Circuit Schema
        circuits_df = pd.DataFrame(sessions) # sessions is from the get_sessions function

        # keep only circuit_key, country_name, country_code
        circuits_df = circuits_df[["circuit_key", "country_name", "country_code"]]

        # check for missing values
        if verbose:
            print(circuits_df.isnull().sum())
            print(circuits_df.head(ROWS))

        # save to csv
        if save:
            circuits_df.to_csv("../../data/cleaned/circuits.csv", index=False)
            return "Success - Data Saved to data/cleaned/circuits.csv"

        return "Success - Data Not Saved"
    except Exception:
        return "Failed - Rate Limited"

def get_driver_api(session_key: int, driver_number: int):
    # sample curl "https://api.openf1.org/v1/drivers?driver_number=1&session_key=9158"
    # sample url: https://api.openf1.org/v1/drivers?driver_number=1&session_key=9158
    driver = requests.get(f"{BASE}/drivers", params = {"driver_number": driver_number, "session_key": session_key}).json()

    return driver

def get_drivers_api(session_key: int):
    drivers = requests.get(f"{BASE}/drivers", params = {"session_key": session_key}).json()

    return drivers

def get_drivers(save = True):
    try:
        if session_df is None or session_df.empty:
            res = get_races(save=save, verbose=False)
            print(f"From get_races subcall: {res}")
            if "Failed" in res:
                return res
                        
        # Drivers Schema
        drivers = []

        for session_key in session_df["session_key"]:
            if session_df.loc[session_df["session_key"] == session_key, "session_type"].values[0] == "Race":
                drivers.extend(get_drivers_api(session_key))

                # add sleep to avoid rate limiting
                time.sleep(1)
            
        # Construct Drivers Table
        drivers_df = pd.DataFrame(drivers)

        # keep only session_key, driver_number, first_name, last_name, team_name
        drivers_df = drivers_df[["session_key", "driver_number", "first_name", "last_name", "team_name"]]

        # check for missing values
        print(drivers_df.isnull().sum())
        print(drivers_df.head(ROWS))

        # save to csv
        if save:
            drivers_df.to_csv("../../data/cleaned/drivers.csv", index=False)
            return "Success - Data Saved to data/cleaned/drivers.csv"

        return "Success - Data Not Saved"
    except Exception:
        return "Failed - Rate Limited"

def get_race_stints_api(session_key: int, driver_num: int):
    # sample curl "https://api.openf1.org/v1/stints?session_key=9165&tyre_age_at_start>=3"
    # sample url: https://api.openf1.org/v1/stints?session_key=9165&tyre_age_at_start>=3 
    stints = requests.get(f"{BASE}/stints", params = {"session_key": session_key, "driver_number": driver_num}).json()
    return stints

def get_race_stints(save = True):
    try:
        if session_df is None or session_df.empty:
            res = get_races(save=save, verbose=False)
            time.sleep(2)
            print(f"From get_races subcall: {res}")
            if "Failed" in res:
                return res
                    
        if race_result_df is None or race_result_df.empty:
            res = get_race_result(save, verbose=False)
            print(f"From get_race_result subcall: {res}")
            if "Failed" in res:
                return res
            
            
        # Race Stints Schema
        race_sessions = session_df.loc[session_df["session_type"] == "Race", "session_key"].tolist()

        mid = len(race_sessions) // 2

        first_batch_sessions = race_sessions[:mid]
        second_batch_sessions = race_sessions[mid:]

        # print("First batch:", len(first_batch_sessions), "sessions")
        # print("Second batch:", len(second_batch_sessions), "sessions")

        stints_1 = []

        for session_key in first_batch_sessions:
            if session_df.loc[session_df["session_key"] == session_key, "session_type"].values[0] == "Race":
                drivers_in_session = race_result_df[race_result_df["session_key"] == session_key]["driver_number"].unique()
                for driver_num in drivers_in_session:
                    stints_data = get_race_stints_api(session_key=session_key, driver_num=driver_num)

                    stints_1.extend(stints_data)

                    time.sleep(1)

        # Construct Stints Table
        stints_df_1 = pd.DataFrame(stints_1)

        # check for missing values
        print(stints_df_1.isnull().sum())
        print("---------------------------------")
        print(stints_df_1.head(ROWS//2))

        # save to csv
        if save:
            stints_df_1.to_csv("../../data/cleaned/stints_part1.csv", index=False)
        
        # break into 2 sections to decrease the chance of rate limiting
        time.slep(10)

        # Race Stints Schema
        stints_2 = []

        for session_key in first_batch_sessions:
            if session_df.loc[session_df["session_key"] == session_key, "session_type"].values[0] == "Race":
                drivers_in_session = race_result_df[race_result_df["session_key"] == session_key]["driver_number"].unique()
                for driver_num in drivers_in_session:
                    stints_data = get_race_stints_api(session_key=session_key, driver_num=driver_num)

                    stints_2.extend(stints_data)

                    time.sleep(1)

        # Construct Stints Table
        stints_df_2 = pd.DataFrame(stints_2)

        # check for missing values
        print(stints_df_2.isnull().sum())
        print("---------------------------------")
        print(stints_df_2.head(ROWS//2))

        # save to csv
        if save:
            stints_df_2.to_csv("../../data/cleaned/stints_part2.csv", index=False)

            stints_df_1 = pd.read_csv("../../data/cleaned/stints_part1.csv")
            stints_df_2 = pd.read_csv("../../data/cleaned/stints_part2.csv")

            laps_df = pd.concat([stints_df_1, stints_df_2], ignore_index=True)

            laps_df.to_csv("../../data/cleaned/stints.csv", index=False)
            return "Success - Data Saved to data/cleaned/stints.csv"

        return "Success - Data Not Saved"
    except Exception:
        return "Failed - Rate Limited"


def get_overtakes_api(session_key: int, driver_num: int):
    # sample curl "https://api.openf1.org/v1/stints?session_key=9165&tyre_age_at_start>=3"
    # sample url: https://api.openf1.org/v1/stints?session_key=9165&tyre_age_at_start>=3 
    overtakes = requests.get(f"{BASE}/overtakes", params = {"session_key": session_key, "overtaking_driver_number": driver_num}).json()
    return overtakes

def get_overtakes(save = True):
    try:
        if session_df is None or session_df.empty:
            res = get_races(save=save, verbose=False)
            print(f"From get_races subcall: {res}")
            if "Failed" in res:
                return res
                        
        # Overtakes Schema
        overtakes = []

        for session_key in session_df["session_key"]:
            if session_df.loc[session_df["session_key"] == session_key, "session_type"].values[0] == "Race":
                drivers_in_session = race_result_df[race_result_df["session_key"] == session_key]["driver_number"].unique()

                for driver_num in drivers_in_session:
                    overtakes_data = get_overtakes_api(session_key=session_key, driver_num=driver_num)
                    overtakes.extend(overtakes_data)
                    time.sleep(0.2)

                # add sleep to avoid rate limiting
                time.sleep(1.5)

        # Construct Overtakes Table
        overtakes_df = pd.DataFrame(overtakes)

        # keep only session_key, overtaking_driver_number
        try:
            overtakes_df = overtakes_df[["session_key", "overtaking_driver_number"]]
        except Exception:
            pass

        # rename driver columns
        overtakes_df = overtakes_df.rename(columns={"overtaking_driver_number": "driver_number"})

        # find all (session_key, driver_number) pairs for race sessions
        race_sessions = session_df.loc[session_df["session_type"] == "Race", "session_key"]

        all_drivers_sessions = race_result_df[race_result_df["session_key"].isin(race_sessions)][["session_key", "driver_number"]].drop_duplicates()
        all_drivers_sessions

        # group by session_key and driver_number and count number of overtakes
        if not overtakes_df.empty:
            overtakes_counts = overtakes_df.groupby(["session_key", "driver_number"]).size().reset_index(name = "num_overtakes")
        else:
            overtakes_counts = pd.DataFrame(columns = ["session_key", "driver_number", "num_overtakes"])

        # merge counts with all drivers, filling missing with 0
        overtakes_df2 = all_drivers_sessions.merge(overtakes_counts, 
                                                on = ["session_key", "driver_number"],
                                                how = "left").fillna({"num_overtakes": 0})

        overtakes_df2["num_overtakes"] = overtakes_df2["num_overtakes"].astype(int)

        # merge session df and overtakes df
        session_lookup = session_df[["session_key", "circuit_key"]]
        overtakes_summary = overtakes_df2.merge(session_lookup, on = "session_key", how = "left")

        # reorder columns to make analysis easier
        overtakes_summary = overtakes_summary[["session_key", "circuit_key", "driver_number", "num_overtakes"]]

        # now, we only want circuit_key, driver_number, and overtake AVERAGE
        circuit_overtakes = overtakes_summary.groupby(["circuit_key", "driver_number"]).agg(overtake_avg = ("num_overtakes", "mean")).reset_index()

        # keep consistent dataframe variable names
        overtakes_df = circuit_overtakes

        # check for missing values
        print(overtakes_df.isnull().sum())
        print("---------------------------------")
        print(overtakes_df.head(ROWS))

        # save to csv
        if save:
            overtakes_df.to_csv("../../data/cleaned/overtakes.csv", index=False)
            return "Success - Data Saved to data/cleaned/overtakes.csv"

        return "Success - Data Not Saved"
    except Exception:
        return "Failed - Rate Limited"


def get_weather_api(session_key: int):
    # sample curl "https://api.openf1.org/v1/weather?meeting_key=1208&wind_direction>=130&track_temperature>=52"
    # sample url: https://api.openf1.org/v1/weather?meeting_key=1208&wind_direction>=130&track_temperature>=52
    weather = requests.get(f"{BASE}/weather", params = {"session_key": session_key}).json()
    return weather

def get_weather(save = True):
    try:
        if session_df is None or session_df.empty:
            res = get_races(save=save, verbose=False)
            print(f"From get_races subcall: {res}")
            if "Failed" in res:
                return res
                        
        # Weather Schema
        weather_rows = []

        for session_key in session_df["session_key"]:
            if session_df.loc[session_df["session_key"] == session_key, "session_type"].values[0] == "Race":
                weather_data = get_weather_api(session_key=session_key)
                weather_rows.extend(weather_data)

                # add sleep to avoid rate limiting
                time.sleep(1)
            
        # Construct Weather Table
        weather_df = pd.DataFrame(weather_rows)

        # keep only session_key, air_temperature, humidity, rainfall, track_temperature, wind_speed, wind_direction
        weather_df = weather_df[["session_key", "air_temperature", "humidity", "rainfall", "track_temperature", "wind_speed", "wind_direction"]]

        # merge in circuit_key
        session_lookup = session_df[["session_key", "circuit_key"]]
        weather_df = weather_df.merge(session_lookup, on = "session_key", how = "left")

        # convert rainfall column into boolean (from int) to match schema
        weather_df["rainfall"] = weather_df["rainfall"].astype(bool)

        # reorder columns to match schema
        weather_df = weather_df[["session_key", "circuit_key", "air_temperature", "humidity", "rainfall", "track_temperature", "wind_speed", "wind_direction"]]

        # check for missing values
        print(weather_df.isnull().sum())
        print("---------------------------------")
        print(weather_df.head(ROWS))


        # save to csv
        if save:
            weather_df.to_csv("../../data/cleaned/weather.csv", index=False)
            return "Success - Data Saved to data/cleaned/weather.csv"

        return "Success - Data Not Saved"
    except Exception:
        return "Failed - Rate Limited"

def get_pirelli_tyre(save = True):
    if circuits_df is None or circuits_df.empty:
        res = get_circuits(save=save, verbose=False)
        if "Failed" in res:
            print(f"From get_circuits subcall: {res}")
            return res

    # Pirelli Tyre Schema
    data = [
        ["Australia", False, "", "", "X", "X", "X", ""],
        ["China", False, "", "X", "X", "X", "", ""],
        ["Japan", False, "X", "X", "X", "", "", ""],
        ["Bahrain", False, "X", "X", "X", "", "", ""],
        ["Saudi Arabia", True, "", "", "X", "X", "X", ""],
        ["Miami", True, "", "", "X", "X", "X", ""],
        ["Emilia-Romagna", True, "", "", "", "X", "X", "X"],
        ["Monaco", True, "", "", "", "X", "X", "X"],
        ["Spain", False, "X", "X", "X", "", "", ""],
        ["Canada", True, "", "", "", "X", "X", "X"],
        ["Austria", False, "", "", "X", "X", "X", ""],
        ["Great Britain", True, "", "X", "X", "X", "", ""],
        ["Belgium", True, "X", "", "X", "X", "", ""],
        ["Hungary", False, "", "", "X", "X", "X", ""],
        ["Netherlands", True, "", "X", "X", "X", "", ""],
        ["Italy", False, "", "", "X", "X", "X", ""],
        ["Azerbaijan", True, "", "", "", "X", "X", "X"],
        ["Singapore", False, "", "", "X", "X", "X", ""],
        ["United States", True, "X", "", "X", "X", "", ""],
        ["Mexico City", True, "", "X", "", "X", "X", ""],
        ["São Paulo", True, "", "X", "X", "X", "", ""],
        ["Las Vegas", False, "", "", "X", "X", "X", ""],
        ["Qatar", False, "X", "X", "X", "", "", ""],
        ["Abu Dhabi", False, "", "", "X", "X", "X", ""],
    ]

    compounds = ["C1", "C2", "C3", "C4", "C5", "C6"]

    name_map = {
        "Australia": "Australia",
        "China": "China",
        "Japan": "Japan",
        "Bahrain": "Bahrain",
        "Saudi Arabia": "Saudi Arabia",
        "Miami": "United States",
        "Las Vegas": "United States",
        "United States": "United States",
        "Emilia-Romagna": "Italy",
        "Monaco": "Monaco",
        "Spain": "Spain",
        "Canada": "Canada",
        "Austria": "Austria",
        "Great Britain": "Great Britain",
        "Belgium": "Belgium",
        "Hungary": "Hungary",
        "Netherlands": "Netherlands",
        "Italy": "Italy",
        "Azerbaijan": "Azerbaijan",
        "Singapore": "Singapore",
        "Mexico City": "Mexico",
        "São Paulo": "Brazil",
        "Qatar": "Qatar",
        "Abu Dhabi": "United Arab Emirates",
    }

    circuits_unique = (
        circuits_df[["circuit_key", "country_name"]]
        .drop_duplicates(subset=["circuit_key", "country_name"])
    )

    country_to_circuit = (
        circuits_unique
        .drop_duplicates(subset=["country_name"])
        .set_index("country_name")["circuit_key"]
        .to_dict()
    )

    YEAR = 2024
    rows = []

    for row in data:
        name = row[0]
        mapped_country = name_map.get(name, name)
        if mapped_country not in country_to_circuit:
            print(f"Warning: no circuit_key found for {name}")
            continue

        circuit_key = country_to_circuit[mapped_country]
        compound_Xs = row[2:]

        for idx, X in enumerate(compound_Xs):
            if X == "X":
                compound = compounds[idx]
                rows.append({
                    "circuit_key": circuit_key,
                    "tyre_compound": compound,
                    "year": YEAR
                })
        
    # Construct Pirelli Tyre Table
    pirelli_df = pd.DataFrame(rows)

    # check for missing values
    print(pirelli_df.isnull().sum())
    print("---------------------------------")
    print(pirelli_df.head(ROWS))


    # save to csv
    if save:
        pirelli_df.to_csv("../../data/cleaned/pirelli_tyre.csv", index=False)
        return "Success - Data Saved to data/cleaned/pirelli_tyre.csv"

    return "Success - Data Not Saved"

