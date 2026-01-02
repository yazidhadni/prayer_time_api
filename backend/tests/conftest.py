import os

# Ensure the limiter is configured to use the test Redis DB before importing app/settings.
os.environ["REDIS_DB"] = "1"

from fastapi.testclient import TestClient
import pytest

from src.app.core.config import settings
from src.app.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True, scope="session")
def set_test_env():
    settings.redis_db = 1


@pytest.fixture(autouse=True)
def clean_redis():
    import redis

    r = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
    )
    r.flushdb()
