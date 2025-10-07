import requests
import pandas as pd
import os

BASE = "https://api.openf1.org/v1"
year = 2025
OUTDIR = "../openf1_testdata"

os.makedirs(OUTDIR, exist_ok=True)

response = requests.get(f"{BASE}/sessions", params={"year": year, "session_name": "Race"})
response.raise_for_status()
sessions = pd.DataFrame(response.json())

#print(sessions)

# get the latest race in the given year
race = sessions.sort_values("date_start").iloc[-1] 
session_key = int(race["session_key"])

meeting = race.get("meeting_official_name", race.get("meeting_name", ""))
circuit = race.get("circuit_short_name", "")
date = pd.to_datetime(race["date_start"]).strftime("%Y-%m-%d")
print(f"Latest race session: {meeting} - {circuit} | {race['session_name']} on {date} (session_key={session_key})")


# get the drivers from the race
drivers = pd.DataFrame(
    requests.get(f"{BASE}/drivers", params={"session_key": session_key}).json()
)
drivers.to_csv(os.path.join(OUTDIR, f"drivers_{session_key}.csv"), index=False)

# getting the lap data
driver_number = int(drivers.iloc[0]["driver_number"])
laps = pd.DataFrame(
    requests.get(f"{BASE}/laps",params={"session_key": session_key, "driver_number": driver_number}).json()
)
laps.to_csv(os.path.join(OUTDIR, f"laps_{session_key}_driver_{driver_number}.csv"), index=False)

# getting stint data
stints = pd.DataFrame(
    requests.get(f"{BASE}/stints", params={"session_key": session_key}).json()
)
stints.to_csv(os.path.join(OUTDIR, f"stints_{session_key}.csv"), index=False)

# getting session result data
session_result = pd.DataFrame(
    requests.get(f"{BASE}/session_result", params={"session_key": session_key}).json()
)
session_result.to_csv(os.path.join(OUTDIR, f"session_result_{session_key}.csv"), index=False)
