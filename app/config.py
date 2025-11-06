from pydantic import BaseSettings, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "AI  Menu Pricing Engine"
    ENV: str = "dev"

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/pricing_db"
    )

    OWM_API_KEY: Optional[str] = None 
    TICKETMASTER_API_KEY: Optional[str] = None

    # Pricing weights & guards.
    
    INTERNAL_WEIGHT: float = 0.6
    EXTERNAL_WEIGHT: float = 0.4
    ROUNDING_STEP: int = 5
    MAX_MARKUP_OVER_MAX_COMP: float = 1.10  # 10% over max competitor
    
    MIN_DISCOUNT_BELOW_MIN_COMP: float = 0.95  # not below 5% of min competitor
    DAILY_CHANGE_CAP_PCT: float = 0.12
    DEFAULT_CITY: str = "Mumbai"
    DEFAULT_LAT: float = 19.0760
    DEFAULT_LON: float = 72.8777

    class Config:
        env_file = ".env"

settings = Settings()