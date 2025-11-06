from sqlalchemy.orm import Session
from ..models import CompetitorPrice
from typing import List


def save_competitor_prices(db: Session, menu_item_id: int, prices: List[float]):
    for p in prices:
        db.add(CompetitorPrice(menu_item_id=menu_item_id, price=p))
    db.commit()