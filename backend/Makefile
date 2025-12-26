dev:
	uv run uvicorn src.prayer_times.main:app --reload

today:
	curl -X GET "http://127.0.0.1:8000/times/today?city="Paris"&country=FR"

test:
	uv run pytest