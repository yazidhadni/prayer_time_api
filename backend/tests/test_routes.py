import datetime
from fastapi.testclient import TestClient

from src.prayer_times.main import app


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
        for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
            assert prayer in data


def test_get_today_prayer_times():
    with TestClient(app) as client:
        today = datetime.date.today()
        response = client.get(
            "/times/today",
            params={
                "country": "FR",
                "city": "Paris",
                "date": today,
            },
        )
        assert response.status_code == 200
        data = response.json()
        for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
            assert prayer in data


def test_invalid_date_format():
    with TestClient(app) as client:
        # FastAPI/Pydantic expects an ISO 8601 date string (YYYY-MM-DD).
        # Passing an invalid format should fail.
        response = client.get(
            "/times",
            params={
                "country": "FR",
                "city": "Paris",
                "date": "30/11/2025",  # Invalid format
            },
        )
        # Should result in a Pydantic validation error
        assert response.status_code == 422
        assert "date" in response.json()["detail"][0]["loc"]


def test_missing_required_params():
    with TestClient(app) as client:
        # Missing 'city' and 'country'
        response = client.get(
            "/times",
            params={
                "date": datetime.date(2025, 11, 30),
            },
        )
        # Should result in a Pydantic validation error
        assert response.status_code == 422

        # Check that the error mentions the missing fields
        details = response.json()["detail"]
        missing_fields = {item["loc"][1] for item in details}
        assert "city" in missing_fields
        assert "country" in missing_fields
