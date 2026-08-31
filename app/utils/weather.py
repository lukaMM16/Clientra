import requests

def get_zagreb_weather():
    # Zagreb lat/lon
    lat, lon = 45.8150, 15.9819
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,wind_speed_10m"
    )
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    current = data.get("current", {})
    return {
        "temperature": current.get("temperature_2m"),
        "wind": current.get("wind_speed_10m"),
        "time": current.get("time"),
    }
