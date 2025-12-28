from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int

    http_timeout: float

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
