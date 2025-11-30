import datetime
from fastapi.testclient import TestClient

from app.main import app


def test_get_prayer_times():
    with TestClient(app) as client:
        response = client.get(
            "/times",
            params={
                "country": "FR",
                "city": "Paris",
                "date": datetime.date(2025, 11, 30),
            },
        )
        assert response.status_code == 200
        data = response.json()
        timings = data["data"]["timings"]
        for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
            assert prayer in timings
