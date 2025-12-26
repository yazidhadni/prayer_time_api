from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str
    # redis_port: int = 6379
    redis_port: int

    # http_timeout: float = 5.0
    http_timeout: float

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
