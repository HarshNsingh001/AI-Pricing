import math
from typing import Iterable

def median(values: Iterable[float]) -> float:
    arr = sorted([v for v in values if v is not None])
    n = len(arr)
    if n == 0:
        return 0.0
    mid = n // 2
    if n % 2 == 0:
        return (arr[mid - 1] + arr[mid]) / 2
    return arr[mid]

def round_to_step(value: float, step: int = 5) -> float:
    return step * round(value / step)

# Haversine distance in km
from math import radians, sin, cos, asin, sqrt

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c