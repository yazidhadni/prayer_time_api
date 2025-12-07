from contextlib import asynccontextmanager
import datetime
import httpx
from fastapi import FastAPI, HTTPException
import logging

from app.schemas import PrayerTimes


BASE_URL = "https://api.aladhan.com/v1"

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=5.0)
    yield
    await app.state.client.aclose()


app = FastAPI(lifespan=lifespan)


@app.get("/times", response_model=PrayerTimes)
async def get_prayer_time(date: datetime.date, city: str, country: str) -> PrayerTimes:
    date_str = date.strftime("%d-%m-%Y")
    params = {"country": country, "city": city}

    try:
        r: httpx.Response = await app.state.client.get(
            f"{BASE_URL}/timingsByCity/{date_str}", params=params, timeout=5.0
        )
        r.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"External API request failed: {e}")

    try:
        data = r.json()
        timings = data["data"]["timings"]
        return PrayerTimes(**timings)
    except Exception as e:
        logger.exception("Failed to parse prayer times")
        raise HTTPException(
            status_code=500, detail="Invalid response from external API"
        )
