import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .api.routes.times import router as times_router
from .core.config import settings
from .core.rate_limit import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=settings.http_timeout)
    app.state.redis = Redis(
        host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
    )

    await app.state.redis.ping()

    yield

    await app.state.client.aclose()
    await app.state.redis.aclose()


app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(times_router, prefix="/times")
