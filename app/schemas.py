from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class WeatherIn(BaseModel):
    temperature: float
    condition: str

class EventIn(BaseModel):
    name: str
    popularity: Literal["Low", "Medium", "High"] = "Low"
    distance_km: float = Field(ge=0)
    starts_at: Optional[str] = None

class SuggestRequest(BaseModel):
    menu_item_id: int
    current_price: float
    competitor_prices: List[float]
    weather: Optional[WeatherIn] = None
    events: Optional[List[EventIn]] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class SuggestResponse(BaseModel):
    menu_item_id: int
    recommended_price: float
    factors: dict
    reasoning: str