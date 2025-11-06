from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    category = Column(String, nullable=True)
    base_price = Column(Float, nullable=True)

class CompetitorPrice(Base):
    __tablename__ = "competitor_prices"
    id = Column(Integer, primary_key=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    competitor_name = Column(String, default="unknown")
    price = Column(Float, nullable=False)
    observed_at = Column(DateTime, default=datetime.utcnow)

class WeatherSnapshot(Base):
    __tablename__ = "weather_snapshots"
    id = Column(Integer, primary_key=True)
    temp_c = Column(Float)
    condition = Column(String)
    source = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    lat = Column(Float)
    lon = Column(Float)
    location_key = Column(String)
    raw = Column(JSON)

class EventSnapshot(Base):
    __tablename__ = "events_snapshots"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    popularity = Column(String)
    distance_km = Column(Float)
    starts_at = Column(DateTime, nullable=True)
    source = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    lat = Column(Float)
    lon = Column(Float)
    raw = Column(JSON)

class PricingRequest(Base):
    __tablename__ = "pricing_requests"
    id = Column(Integer, primary_key=True)
    menu_item_id = Column(Integer)
    payload_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class PricingRecommendation(Base):
    __tablename__ = "pricing_recommendations"
    id = Column(Integer, primary_key=True)
    pricing_request_id = Column(Integer, ForeignKey("pricing_requests.id"))
    recommended_price = Column(Float)
    internal_weight = Column(Float)
    external_weight = Column(Float)
    reasoning = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)