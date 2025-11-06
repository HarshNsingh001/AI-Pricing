import requests
from ..config import settings
from ..utils import haversine_km

TM_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def fetch_events(lat: float, lon: float, radius_km: float = 10):
    if not settings.TICKETMASTER_API_KEY:
        return []
    params = {
        "apikey": settings.TICKETMASTER_API_KEY,
        "latlong": f"{lat},{lon}",
        "radius": max(1, int(radius_km)),
        "unit": "km",
        "size": 10,
        "sort": "date,asc",
    }
    r = requests.get(TM_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    events = []
    for item in (data.get("_embedded", {}) or {}).get("events", [])[:10]:
        name = item.get("name")
        venues = (item.get("_embedded", {}) or {}).get("venues", [])
        if venues:
            v = venues[0]
            vlat = float(v.get("location", {}).get("latitude", lat))
            vlon = float(v.get("location", {}).get("longitude", lon))
            d = haversine_km(lat, lon, vlat, vlon)
        else:
            d = 999
        # Derive a crude popularity
        seg = (item.get("classifications", [{}])[0] or {}).get("segment", {}).get("name", "")
        pop = "High" if seg in ("Sports", "Music") else "Medium"
        events.append({
            "name": name,
            "popularity": pop,
            "distance_km": round(d, 2),
            "starts_at": item.get("dates", {}).get("start", {}).get("dateTime"),
            "raw": item,
        })
    return events