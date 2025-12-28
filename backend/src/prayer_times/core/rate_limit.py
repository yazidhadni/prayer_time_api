from slowapi import Limiter
from slowapi.util import get_remote_address

from .config import settings


limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
)
