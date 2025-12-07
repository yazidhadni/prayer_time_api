import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api.routes.times import router as times_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=5.0)
    yield
    await app.state.client.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(times_router)
