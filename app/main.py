from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routers import pricing, ingest
from .config import settings

# auto create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)


@app.get("/health")
def health():
    
    return {
        "status": "ok",
        "db": settings.DATABASE_URL.split(":")[0],
        "owm_key_loaded": bool(settings.OWM_API_KEY),
        "tm_key_loaded": bool(settings.TICKETMASTER_API_KEY),
        
    }


app.include_router(ingest.router)
app.include_router(pricing.router)
