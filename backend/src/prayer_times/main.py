import httpx
from functools import lru_cache
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis

from .api.routes.times import router as times_router
from .core.config import settings


# @lru_cache
# def get_settings():
#     return settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=settings.http_timeout)
    app.state.redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
    )

    await app.state.redis.ping()

    yield

    await app.state.client.aclose()
    await app.state.redis.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(times_router, prefix="/times")
