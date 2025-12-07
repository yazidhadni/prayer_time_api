import datetime
from fastapi import APIRouter, HTTPException, Request

from src.prayer_times.services.prayer_time_service import fetch_prayer_times
from src.prayer_times.schemas import PrayerTimes

router = APIRouter()


@router.get("/times", response_model=PrayerTimes)
async def get_prayer_time(
    request: Request, date: datetime.date, city: str, country: str
) -> PrayerTimes:
    try:
        return await fetch_prayer_times(
            client=request.app.state.client, date=date, city=city, country=country
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
