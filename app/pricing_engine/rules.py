from typing import List, Tuple
from ..utils import median, round_to_step
from ..config import settings

# Weather multiplier based on simple rules

def weather_multiplier(temp_c: float, condition: str) -> float:
    condition = (condition or "").lower()
    if condition in ["rain", "thunderstorm", "drizzle"]:
        return 1.06
    if condition in ["sunny", "clear"] and temp_c >= 30:
        return 1.08
    if condition in ["snow"]:
        return 1.04
    return 1.00

# Events multiplier combining popularity and distance decay

def events_multiplier(events: List[dict]) -> float:
    if not events:
        return 1.0
    pop_map = {"Low": 1.00, "Medium": 1.05, "High": 1.12}
    mult = 1.0
    for e in events:
        base = pop_map.get(e.get("popularity", "Low"), 1.0)
        d = float(e.get("distance_km", 999))
        decay = max(0.7, 1 - (d / 10.0))
        mult *= (base * decay)
    return min(mult, 1.25)

# Core recommendation logic

def recommend_price(current_price: float, competitor_prices: List[float], weather: dict | None, events: List[dict] | None) -> Tuple[float, dict, str]:
    comp_med = median(competitor_prices)
    internal_anchor = 0.5 * current_price + 0.5 * comp_med if comp_med > 0 else current_price

    w_mult = weather_multiplier(weather.get("temperature", 0), weather.get("condition", "")) if weather else 1.0
    e_mult = events_multiplier(events or [])
    external_mult = w_mult * e_mult

    iw = settings.INTERNAL_WEIGHT
    ew = settings.EXTERNAL_WEIGHT

    raw = internal_anchor * (iw + ew * external_mult)

    # Guards vs competitors
    cmin, cmax = min(competitor_prices), max(competitor_prices)
    guard_min = cmin * settings.MIN_DISCOUNT_BELOW_MIN_COMP
    guard_max = cmax * settings.MAX_MARKUP_OVER_MAX_COMP

    guarded = min(max(raw, guard_min), guard_max)
    final_price = round_to_step(guarded, step=settings.ROUNDING_STEP)

    reasoning = []
    if weather:
        reasoning.append(f"Weather {weather.get('condition')} {weather.get('temperature')}°C → x{w_mult:.2f}")
    if events:
        reasoning.append(f"Events impact → x{e_mult:.2f}")
    reasoning.append(f"Internal anchor based on current & competitors → {internal_anchor:.2f}")

    factors = {
        "internal_weight": iw,
        "external_weight": ew,
        "weather_multiplier": round(w_mult, 3),
        "events_multiplier": round(e_mult, 3),
    }

    return float(final_price), factors, "; ".join(reasoning)