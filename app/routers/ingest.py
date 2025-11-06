# app/routers/ingest.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.competitors import save_competitor_prices
from ..models import MenuItem

router = APIRouter(prefix="/api/ingest", tags=["ingest"])

class CompetitorsIn(BaseModel):
    menu_item_id: int
    competitor_prices: List[float]

@router.post("/competitors")
def ingest_competitors(payload: CompetitorsIn, db: Session = Depends(get_db)):
    # ensure menu item exists to avoid FK errors
    mi = db.query(MenuItem).filter(MenuItem.id == payload.menu_item_id).first()
    if not mi:
        db.add(
            MenuItem(
                id=payload.menu_item_id,
                name=f"Item-{payload.menu_item_id}",
                category="NA",
                base_price=None,
            )
        )
        db.commit()

    try:
        save_competitor_prices(db, payload.menu_item_id, payload.competitor_prices)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save competitor prices: {e}")

    return {
        "status": "ok",
        "menu_item_id": payload.menu_item_id,
        "inserted": len(payload.competitor_prices),
    }
