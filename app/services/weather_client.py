import requests
from ..config import settings

OWM_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(lat: float | None = None, lon: float | None = None, city: str | None = None):
    if not settings.OWM_API_KEY:
        return None
    params = {
        "appid": settings.OWM_API_KEY,
        "units": "metric",
    }
    if lat and lon:
        params.update({"lat": lat, "lon": lon})
    else:
        params.update({"q": city or settings.DEFAULT_CITY})
    r = requests.get(OWM_URL, params=params, timeout=8)
    r.raise_for_status()
    data = r.json()
    temp = data.get("main", {}).get("temp")
    condition = (data.get("weather", [{}])[0] or {}).get("main", "")
    return {
        "temperature": temp,
        "condition": condition,
        "raw": data,
    }