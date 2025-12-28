import datetime


def test_rate_limiting(client):
    for _ in range(5):
        response = client.get(
            "/times",
            params={
                "date": datetime.date.today(),
                "country": "FR",
                "city": "Paris",
            },
        )
        assert response.status_code == 200

    response = client.get(
        "/times",
        params={
            "date": datetime.date.today(),
            "country": "FR",
            "city": "Paris",
        },
    )
    assert response.status_code == 429
