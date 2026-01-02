import datetime
from fastapi import APIRouter, HTTPException, Request

# from src.prayer_times.core.rate_limit import limiter
# from src.prayer_times.services import prayer_time_service
# from src.prayer_times.schemas import PrayerTimes

from app.core.rate_limit import limiter
from app.services import prayer_time_service
from app.schemas import PrayerTimes


router = APIRouter()


@router.get("", response_model=PrayerTimes)
@limiter.limit("5/minute")
async def get_prayer_time(
    request: Request, date: datetime.date, city: str, country: str
) -> PrayerTimes:
    try:
        prayers = await prayer_time_service.get_prayer_times(
            client=request.app.state.client,
            redis=request.app.state.redis,
            date=date,
            city=city,
            country=country,
        )
        return prayers.prayer_times
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/today", response_model=PrayerTimes)
@limiter.limit("5/minute")
async def get_today_prayer_time(
    request: Request, city: str, country: str
) -> PrayerTimes:
    """Return prayer times for today."""
    today = datetime.date.today()
    try:
        prayers = await prayer_time_service.get_prayer_times(
            client=request.app.state.client,
            redis=request.app.state.redis,
            date=today,
            city=city,
            country=country,
        )
        return prayers.prayer_times
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
