from typing import List, Tuple
import json, os

COEFFS_PATH = os.getenv("ML_COEFFS_PATH", "./ml_coeffs.json")

FEATURES = [
    "bias",
    "current_price",
    "comp_median",
    "comp_std",
    "temp_c",
    "is_hot",
    "is_rain",
    "top_event_popularity",
    "min_event_distance",
]

def load_coeffs():
    with open(COEFFS_PATH, "r") as f:
        return json.load(f)

from statistics import median, pstdev

def featureize(current_price: float, competitor_prices: List[float], weather: dict | None, events: List[dict] | None):
    comp_med = median(competitor_prices) if competitor_prices else 0
    comp_std = pstdev(competitor_prices) if len(competitor_prices) > 1 else 0
    temp = (weather or {}).get("temperature", 0)
    cond = (weather or {}).get("condition", "").lower()
    is_hot = 1 if temp >= 30 else 0
    is_rain = 1 if cond in ["rain", "thunderstorm", "drizzle"] else 0

    pops = {"Low": 0, "Medium": 1, "High": 2}
    top_pop = max([pops.get(e.get("popularity", "Low"), 0) for e in (events or [])] or [0])
    min_dist = min([e.get("distance_km", 999) for e in (events or [])] or [999])

    feats = {
        "bias": 1,
        "current_price": current_price,
        "comp_median": comp_med,
        "comp_std": comp_std,
        "temp_c": temp,
        "is_hot": is_hot,
        "is_rain": is_rain,
        "top_event_popularity": top_pop,
        "min_event_distance": min_dist,
    }
    return feats


def recommend_price_ml(current_price: float, competitor_prices: List[float], weather: dict | None, events: List[dict] | None) -> Tuple[float, dict, str]:
    coeffs = load_coeffs()  # dict of feature->weight
    feats = featureize(current_price, competitor_prices, weather, events)
    pred = 0.0
    for k, v in feats.items():
        w = coeffs.get(k, 0)
        pred += w * v
    factors = {"model": "linear", "coefficients_used": {k: coeffs.get(k, 0) for k in feats}}
    return float(pred), factors, "ML linear regression prediction"