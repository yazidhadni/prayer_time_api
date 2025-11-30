from contextlib import asynccontextmanager
import datetime
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient


BASE_URL = "https://api.aladhan.com/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient()
    yield
    await app.state.client.aclose()


app = FastAPI(lifespan=lifespan)


@app.get("/times")
async def get_prayer_time(date: datetime.date, city: str, country: str):
    date_str = date.strftime("%d-%m-%Y")
    params = {"country": country, "city": city}

    try:
        r = await app.state.client.get(
            f"{BASE_URL}/timingsByCity/{date_str}", params=params
        )
        r.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to API: {e}")

    return r.json()
