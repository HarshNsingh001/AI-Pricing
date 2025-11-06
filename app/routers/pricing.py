from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import SuggestRequest, SuggestResponse
from ..database import get_db
from ..models import PricingRequest, PricingRecommendation, WeatherSnapshot, EventSnapshot
from ..pricing_engine.rules import recommend_price as rules_recommend
from ..pricing_engine.ml import recommend_price_ml
from ..config import settings
from ..services.weather_client import fetch_weather
from ..services.events_client import fetch_events

router = APIRouter(prefix="/api/pricing", tags=["pricing"])


@router.post("/suggest", response_model=SuggestResponse)
def suggest_price(req: SuggestRequest, db: Session = Depends(get_db)):

    # persist incoming payload
    pr = PricingRequest(menu_item_id=req.menu_item_id, payload_json=req.dict())
    db.add(pr)
    db.commit()
    db.refresh(pr)

    # default lat/lon
    lat = req.lat or settings.DEFAULT_LAT
    lon = req.lon or settings.DEFAULT_LON

    # weather
    weather = req.weather.dict() if req.weather else None
    if weather is None:
        try:
            w = fetch_weather(lat=lat, lon=lon)
            if w and w.get("temperature") is not None:
                weather = {
                    "temperature": w["temperature"],
                    "condition": w.get("condition", "")
                }
                try:
                    db.add(
                        WeatherSnapshot(
                            temp_c=w["temperature"],
                            condition=w.get("condition", ""),
                            source="OWM",
                            lat=lat,
                            lon=lon,
                            location_key=f"{lat},{lon}",
                            raw=w.get("raw")
                        )
                    )
                    db.commit()
                except:
                    db.rollback()
        except:
            weather = None

    # events
    events = [e.dict() for e in req.events] if req.events else None
    if events is None:
        try:
            events = fetch_events(lat=lat, lon=lon)
            if events:
                try:
                    for e in events:
                        db.add(
                            EventSnapshot(
                                name=e.get("name"),
                                popularity=e.get("popularity"),
                                distance_km=e.get("distance_km"),
                                starts_at=None,
                                source="Ticketmaster",
                                lat=lat,
                                lon=lon,
                                raw=e.get("raw"),
                            )
                        )
                    db.commit()
                except:
                    db.rollback()
        except:
            events = []

    # ml first, fallback to rules
    try:
        rec, extra_factors, ml_reason = recommend_price_ml(
            req.current_price, req.competitor_prices, weather, events
        )
        factors = {
            "internal_weight": settings.INTERNAL_WEIGHT,
            "external_weight": settings.EXTERNAL_WEIGHT,
            **extra_factors
        }
        reasoning = ml_reason
        recommended_price = rec
    except:
        recommended_price, factors, reasoning = rules_recommend(
            req.current_price, req.competitor_prices, weather, events
        )

    # save recommendation
    try:
        rec_row = PricingRecommendation(
            pricing_request_id=pr.id,
            recommended_price=recommended_price,
            internal_weight=factors.get("internal_weight", settings.INTERNAL_WEIGHT),
            external_weight=factors.get("external_weight", settings.EXTERNAL_WEIGHT),
            reasoning=reasoning,
        )
        db.add(rec_row)
        db.commit()
    except:
        db.rollback()

    return SuggestResponse(
        menu_item_id=req.menu_item_id,
        recommended_price=float(recommended_price),
        factors={
            "internal_weight": settings.INTERNAL_WEIGHT,
            "external_weight": settings.EXTERNAL_WEIGHT
        },
        reasoning=reasoning,
    )
