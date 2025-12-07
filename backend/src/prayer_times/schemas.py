import pydantic


class PrayerTimes(pydantic.BaseModel):
    Fajr: str
    Dhuhr: str
    Asr: str
    Maghrib: str
    Isha: str
