import datetime
import httpx
import logging

from src.prayer_times.schemas import PrayerTimes

logger = logging.getLogger(__name__)
BASE_URL = "https://api.aladhan.com/v1"


async def fetch_prayer_times(
    client: httpx.AsyncClient, date: datetime.date, city: str, country: str
) -> PrayerTimes:
    date_str = date.strftime("%d-%m-%Y")
    params = {"country": country, "city": city}

    try:
        response: httpx.Response = await client.get(
            f"{BASE_URL}/timingsByCity/{date_str}", params=params
        )
        response.raise_for_status()
    except httpx.RequestError as e:
        raise RuntimeError(f"External API request failed: {e}")

    try:
        data = response.json()
        timings = data["data"]["timings"]
        return PrayerTimes(**timings)
    except Exception as e:
        logger.exception("Failed to parse prayer times")
        raise RuntimeError("Invalid response from external API")
