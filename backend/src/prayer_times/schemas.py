import pydantic


class PrayerTimes(pydantic.BaseModel):
    Fajr: str
    Dhuhr: str
    Asr: str
    Maghrib: str
    Isha: str


class PrayerDay(pydantic.BaseModel):
    prayer_times: PrayerTimes
    date: str  # date in ISO format
