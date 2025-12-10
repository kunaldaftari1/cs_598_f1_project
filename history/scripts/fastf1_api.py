import fastf1 as f1
import os

cache_dir = os.path.join("fastf1_testdata", "cache_fastf1")
raw_dir = os.path.join("fastf1_testdata", "raw")
os.makedirs(cache_dir, exist_ok = True)
os.makedirs(raw_dir, exist_ok = True)

f1.Cache.enable_cache(cache_dir)

session = f1.get_session(2024, "Monaco", "R")
session.load()

print(session.event['EventName'], session.event['EventDate'])
print(session.results.iloc[:5][['DriverNumber','Abbreviation','Position','Points']])

out_csv = os.path.join(raw_dir, "fastf1_monaco_2024_results.csv")
session.results.to_csv(out_csv, index=False)
print("Saved:", out_csv)