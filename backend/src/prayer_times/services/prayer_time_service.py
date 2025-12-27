import datetime
import httpx
import logging

from redis import Redis

from src.prayer_times.schemas import PrayerTimes, PrayerDay

logger = logging.getLogger(__name__)
BASE_URL = "https://api.aladhan.com/v1"
CACHE_TTL_SECONDS = 60 * 60  # 1 hour


def _get_cache_key(country: str, city: str, date: datetime.date):
    return f"prayer_times:{country.lower()}:{city.lower()}:{date.isoformat()}"


async def _fetch_prayer_times_api(
    client: httpx.AsyncClient, date: datetime.date, city: str, country: str
) -> PrayerDay:
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
        prayers_times = PrayerTimes(**timings)
        return PrayerDay(prayer_times=prayers_times, date=date)
    except Exception as e:
        logger.exception("Failed to parse prayer times")
        raise RuntimeError("Invalid response from external API")


async def get_prayer_times(
    *,
    client: httpx.AsyncClient,
    redis: Redis,
    date: datetime.date,
    city: str,
    country: str,
) -> PrayerDay:
    cache_key = _get_cache_key(country=country, city=city, date=date)
    cached = await redis.get(cache_key)
    if cached:
        return PrayerDay.model_validate_json(cached)

    try:
        prayers: PrayerDay = await _fetch_prayer_times_api(
            client=client, date=date, city=city, country=country
        )
    except httpx.HTTPError as e:
        logger.exception("External API call failed")
        raise RuntimeError("External API request failed") from e

    await redis.set(cache_key, prayers.model_dump_json(), ex=CACHE_TTL_SECONDS)

    return prayers
