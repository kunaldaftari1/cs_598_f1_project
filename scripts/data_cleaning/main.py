import factory
import sys
import time
import pandas as pd
import os


DATE = None
TIME = 2
ROWS = 25

def handle_args(args):
    # Parse and handle to_save argument

    to_save = args[0].lower()
    if to_save == "false":
        to_save = False
    elif to_save == "true":
        to_save = True
    else:
        print("Invalid value for argument 1.")
        print("Try: True/False")
    
    return to_save

def assisted_method():
    global DATE

    print("=================================")
    print("Assisted Mode")
    print("=================================")

    while True:
        cmd = input("Which of the following methods would you like to call: \n" \
        "- races \n" \
        "- starting_grid (grid) \n" \
        "- race_result (result) \n" \
        "- circuits \n" \
        "- drivers \n" \
        "- race_stints (stints) \n" \
        "- overtakes \n" \
        "- weather \n" \
        "- pirelli_tyres (tyres) \n" \
        "Enter command (function/date/rows/exit): ")
        
        print("---------------------------------")

        if cmd.lower() == "exit":
            print("Exiting.")
            break

        if cmd.lower() == "function":
            print("Please enter a function from the provided list.")
            continue

        if cmd.lower() == "rows":
            num_rows = input("How many rows of data should be printed: ")
            if num_rows.isdigit():
                factory.update_rows(int(num_rows))
                print("---------------------------------")
                continue
            else:
                print("Invalid input.")
                continue
        
        if cmd.lower() == "date" or DATE is None:
            DATE = input("Oldest data to use (YYYY-MM-DD): ")
            res = factory.get_races(False, DATE, False)

            if "Failed" in res:
                print("Rate Limited... try again later.")
                continue

            if cmd.lower() == "date":
                continue

        to_save = input("Would you like to save the data? \nEnter (yes\\no): ")
        if to_save == "yes" or to_save == "y":
            to_save = True
        elif to_save == "no" or to_save == "n":
            to_save = False
        else:
            print("Incorrect value for argument.")
            break
        
        print("---------------------------------")

        if cmd == "races":
            result = factory.get_races(to_save, DATE)     
        elif cmd == "starting_grid" or cmd == "grid":
            result = factory.get_starting_grid(to_save)  
        elif cmd == "race_result" or cmd == "result":
            result = factory.get_race_result(to_save)
        elif cmd == "circuits" or cmd == "circuit":
            result = factory.get_circuits(to_save)
        elif cmd == "drivers":
            result = factory.get_drivers(to_save)
        elif cmd == "stints" or cmd == "race_stints":
            result = factory.get_race_stints(to_save)
        elif cmd == "overtakes":
            result = factory.get_overtakes(to_save)
        elif cmd == "weather":
            result = factory.get_weather(to_save)
        elif cmd == "pirelli_tyre" or cmd == "pirelli_tire" or cmd == "pirelli" or cmd == "tyre" or cmd == "tire":
            result = factory.get_pirelli_tyre(to_save)      
        else:
            print("Invalid command.")
            print("=================================")    
            continue      

        print("---------------------------------")
        print(f"Result: {result}")
        print("=================================")
        continue
    
    print("=================================")

    
def manual_method():
    global DATE

    print("=================================")
    print("Manual Mode")
    print("=================================")

    while True:
        command = input("Enter command: ").strip()
        print("---------------------------------")

        if command.lower() == "exit":
            print("Exiting.")
            break

        parts = command.split()
        
        if len(parts) == 0:
            print("No command provided.")
            continue

        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "rows":
            if len(args) == 0:
                print("Invalid arguments.")
                continue

            num_rows = args[0]
            if num_rows.isdigit():
                factory.update_rows(int(num_rows))
                print("Rows updated.")
                print("---------------------------------")
            else:
                print("Invalid input.")
                
            continue

        elif cmd == "date":
            if len(args) == 0:
                print("Invalid arguments.")
                continue

            DATE = args[0]
            res = factory.get_races(False, DATE, False)

            if "Failed" in res:
                print("Rate Limited... try again later.")

            continue

        elif cmd == "races":
            if len(args) == 0:
                if DATE is not None:
                    result = factory.get_races(date_start=DATE)
                else:
                    result = factory.get_races()
            else:
                to_save = handle_args(args)
                if DATE is not None:
                    result = factory.get_races(to_save, date_start=DATE)     
                else:
                    result = factory.get_races(to_save)

        elif cmd == "starting_grid" or cmd == "grid":
            if len(args) == 0:
                result = factory.get_starting_grid()
            else:
                to_save = handle_args(args)
                result = factory.get_starting_grid(to_save)  
        elif cmd == "race_result" or cmd == "result":
            if len(args) == 0:
                result = factory.get_race_result()
            else:
                to_save = handle_args(args)
                result = factory.get_race_result(to_save)
        elif cmd == "circuits" or cmd == "circuit":
            if len(args) == 0:
                result = factory.get_circuits()
            else:
                to_save = handle_args(args)
                result = factory.get_circuits(to_save)
        elif cmd == "drivers":
            if len(args) == 0:
                result = factory.get_drivers()
            else:
                to_save = handle_args(args)
                result = factory.get_drivers(to_save)
        elif cmd == "stints" or cmd == "race_stints":
            if len(args) == 0:
                result = factory.get_race_stints()
            else:
                to_save = handle_args(args)
                result = factory.get_race_stints(to_save)
        elif cmd == "overtakes":
            if len(args) == 0:
                result = factory.get_overtakes()
            else:
                to_save = handle_args(args)
                result = factory.get_overtakes(to_save)
        elif cmd == "weather":
            if len(args) == 0:
                result = factory.get_weather()
            else:
                to_save = handle_args(args)
                result = factory.get_weather(to_save)
        elif cmd == "pirelli_tyre" or cmd == "pirelli_tire" or cmd == "pirelli" or cmd == "tyre" or cmd == "tire":
            if len(args) == 0:
                result = factory.get_pirelli_tyre()
            else:
                to_save = handle_args(args)
                result = factory.get_pirelli_tyre(to_save)      
        else:
            print("Invalid command.")
            print("=================================")    
            continue      
        
        print("---------------------------------")
        print(f"Result: {result}")
        print("=================================")
        continue

    print("=================================")

def load_cleaned(name: str):
    PATH = "../../data/cleaned/"
    path = PATH + name + ".csv"

    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None
    
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"Failed to read {path} with error: {e}")
        return None

    return df.head(ROWS)
    

def pre_process():
    global ROWS

    print("=================================")
    print("Pre-Generated Data Mode")
    print("=================================")
    print("Command Options: \n" \
    "- races \n" \
    "- starting_grid (grid) \n" \
    "- race_result (result) \n" \
    "- circuits \n" \
    "- drivers \n" \
    "- race_stints (stints) \n" \
    "- overtakes \n" \
    "- weather \n" \
    "- pirelli_tyres (tyres) \n" \
    "- rows [int] \n"
    "- exit")


    while True:
        command = input("Enter command: ").strip()
        print("---------------------------------")

        if command.lower() == "exit":
            print("Exiting.")
            break
        
        parts = command.split()
        if len(parts) == 0:
            print("No command provided.")
            continue

        cmd = parts[0].lower()
        args = parts[1:]

        # change the number of rows shown
        if cmd == "rows":
            if len(args) == 0:
                print("Invalid arguments.")
                continue
            num_rows = args[0]
            if num_rows.isdigit():
                ROWS = int(num_rows)
                print(f"Rows updated to {ROWS}")
                print("---------------------------------")
            else:
                print("Invalid input for rows.")
            continue
        
        if cmd == "races":
            result = load_cleaned("sessions")
        elif cmd == "starting_grid" or cmd == "grid":
            result = load_cleaned("starting_grid")
        elif cmd == "race_result" or cmd == "result":
            result = load_cleaned("race_result")
        elif cmd == "circuits" or cmd == "circuit":
            result = load_cleaned("circuits")
        elif cmd == "drivers":
            result = load_cleaned("drivers")
        elif cmd == "stints" or cmd == "race_stints":
            result = load_cleaned("stints")
        elif cmd == "overtakes":
            result = load_cleaned("overtakes")
        elif cmd == "weather":
            result = load_cleaned("weather")
        elif cmd == "pirelli_tyre" or cmd == "pirelli_tire" or cmd == "pirelli" or cmd == "tyre" or cmd == "tire":
            result = load_cleaned("pirelli_tyre")
        else:
            print("Invalid command.")
            print("=================================")    
            continue      
        
        print("---------------------------------")
        print("Result:")
        print(result)
        print("=================================")
    
    print(("================================="))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [manual (m) | assisted (a) | pre-generated (p)]")

        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "manual" or mode == "m":
        manual_method()
    elif mode == "assisted" or mode == "a":
        assisted_method()
    elif mode == "pre-generated" or mode == "p" or mode == "pg":
        pre_process()
    else:
        print("Invalid input.")


