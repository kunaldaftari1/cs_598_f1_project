# AI ASSISTED CODE
import os, time
import requests
import pandas as pd
from datetime import timedelta

BASE = "https://api.openf1.org/v1"
YEAR = 2025
OUTDIR = "../openf1_samples"
DRIVER_LIMIT = 1            # how many drivers to sample for driver-scoped endpoints
WINDOW_MINUTES = 5          # time-box per-driver pulls to avoid 422s
SLEEP_BETWEEN_CALLS = 1.0  # be polite to the API

os.makedirs(OUTDIR, exist_ok=True)

def get(endpoint, **params):
    r = requests.get(f"{BASE}/{endpoint}", params=params, timeout=60)
    if r.ok:
        return r.json(), None, r.status_code
    return None, (r.text or "").strip()[:800], r.status_code

def save_csv(df, path):
    if df is not None and not df.empty:
        df.to_csv(path, index=False)
        print(f"[saved] {path} (rows={len(df)})")

def df_or_empty(js): return pd.DataFrame(js) if js else pd.DataFrame()

print("=== OpenF1 sampler -> CSVs ===")

# 1) Target session (latest Race in YEAR)
js, err, code = get("sessions", year=YEAR, session_name="Race")
if js is None:
    raise SystemExit(f"[fatal] sessions failed ({code}): {err}")
sessions = pd.DataFrame(js)
race = sessions.sort_values("date_start").iloc[-1]
session_key = int(race["session_key"])
meeting = race.get("meeting_official_name", race.get("meeting_name", ""))
circuit = race.get("circuit_short_name", "")
date_start = pd.to_datetime(race["date_start"])
date_end = pd.to_datetime(race.get("date_end", race["date_start"]))
print(f"Target: {meeting} - {circuit} | {race['session_name']} ({session_key})")

# 2) Drivers (choose sample set for per-driver endpoints)
js, err, code = get("drivers", session_key=session_key)
drivers = df_or_empty(js).sort_values("driver_number")
save_csv(drivers, os.path.join(OUTDIR, f"drivers_{session_key}.csv"))
driver_numbers = drivers["driver_number"].astype(int).tolist()[:DRIVER_LIMIT] if not drivers.empty else []
print(f"[info] sampling drivers: {driver_numbers}\n")

# 3) Session-wide endpoints — single CSV each
session_eps = ["stints","session_result","intervals","pit","race_control","weather","starting_grid","overtakes"]
for ep in session_eps:
    js, err, code = get(ep, session_key=session_key)
    if js is None:
        print(f"[warn] {ep} ({code}): {err}")
        continue
    df = df_or_empty(js)
    save_csv(df, os.path.join(OUTDIR, f"{ep}_{session_key}.csv"))
    time.sleep(SLEEP_BETWEEN_CALLS)

# 4) Driver-scoped endpoints — time-boxed window to avoid 422
driver_eps = ["laps","car_data","position","location","team_radio"]
t0, t1 = date_start, date_start + timedelta(minutes=WINDOW_MINUTES)

for ep in driver_eps:
    if not driver_numbers:
        print(f"[info] skipping {ep}: no drivers found"); continue
    for dn in driver_numbers:
        params = {
            "session_key": session_key,
            "driver_number": int(dn),
            "date>=": t0.isoformat(),
            "date<":  t1.isoformat(),
        }
        js, err, code = get(ep, **params)
        # If the window still errors (e.g., 422), try unfiltered once
        if js is None:
            print(f"[info] {ep} d{dn} windowed fetch {code}. Trying unfiltered once…")
            js2, err2, code2 = get(ep, session_key=session_key, driver_number=int(dn))
            js, err, code = (js2, err2, code2)

        if js is None:
            print(f"[warn] {ep} d{dn} failed ({code}): {err}")
            continue

        df = df_or_empty(js)
        out = os.path.join(OUTDIR, f"{ep}_{session_key}_driver_{dn}.csv")
        save_csv(df, out)
        time.sleep(SLEEP_BETWEEN_CALLS)

# 5) Meeting/context (nice to have)
meet_key = int(race["meeting_key"])
js, err, code = get("sessions", meeting_key=meet_key)
save_csv(df_or_empty(js), os.path.join(OUTDIR, f"sessions_meeting_{meet_key}.csv"))

js, err, code = get("meetings", year=YEAR, meeting_key=meet_key)
save_csv(df_or_empty(js), os.path.join(OUTDIR, f"meetings_{meet_key}.csv"))

print("\n=== done ===\nNotes:")
print(f"- Saved to: {os.path.abspath(OUTDIR)}")
print(f"- Driver endpoints limited to first {DRIVER_LIMIT} drivers and {WINDOW_MINUTES} min window.")
print("- Increase DRIVER_LIMIT/WINDOW_MINUTES if you need more, but heavy pulls may 422.")
