import os
import requests
import pandas as pd

OUTDIR = "../openmeteo_testdata"
CITY = "Monaco"
COUNTRY = "MC"
os.makedirs(OUTDIR, exist_ok=True)

response = requests.get(
    "https://geocoding-api.open-meteo.com/v1/search",
    params={"name": CITY, "count": 5, "language": "en", "format": "json"},
    timeout=30,
)
response.raise_for_status()
geo = response.json()

results = geo.get("results", [])

candidates = [r for r in results if r.get("country_code") == COUNTRY]
place = candidates[0] if candidates else results[0]

# print(candidates)
print("Chosen place:", place)

lat, lon = float(place["latitude"]), float(place["longitude"])

print(f"Coordinates: ({lat}, {lon})")

# forecast request example
# https://open-meteo.com/en/docs
forecast_response = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": lat, "longitude": lon, "timezone": "auto",
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    },
    timeout=30,
)

forecast_response.raise_for_status()
forecast = forecast_response.json()

# error handling
hourly = pd.DataFrame(forecast.get("hourly", {}))
daily  = pd.DataFrame(forecast.get("daily", {}))

# we need the dates to be in pandas format
if not hourly.empty and "time" in hourly:
    hourly["time"] = pd.to_datetime(hourly["time"])
if not daily.empty and "time" in daily:
    daily["time"] = pd.to_datetime(daily["time"])

hourly.to_csv(os.path.join(OUTDIR, "forecast_hourly.csv"), index=False)
daily.to_csv(os.path.join(OUTDIR, "forecast_daily.csv"), index=False)
