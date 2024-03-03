from multiprocessing import cpu_count
from typing import Dict, Any

from pydantic import Field
from pydantic_settings import BaseSettings


class BaseEnvSettings(BaseSettings):
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


class ServerSettings(BaseEnvSettings):
    NAME: str = "ff_server"
    HOST: str = "0.0.0.0"
    ENV_MODE: str = "dev"
    VERSION: str = "0.0.1"
    PORT: int = 6969
    LOG_LEVEL: str = "debug"
    RELOAD: bool = True
    WORKERS: int = cpu_count() * 2 - 1 if ENV_MODE == "prod" else 1
    KEEPALIVE: int = 65

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "openapi_prefix": "",
            "redoc_url": None,
            "docs_url": None if self.ENV_MODE != "dev" else "/docs",
            "openapi_url": None if self.ENV_MODE != "dev" else "/openapi.json",
            "openapi_tags": (
                None
                if self.ENV_MODE != "dev"
                else [{"name": "monitor", "description": "uptime monitor endpoints"}]
            ),
        }


class RedisSettings(BaseEnvSettings):
    # REDIS_URL: str = "redis://161.35.18.155:8568/0"
    REDIS_HOST: str = "161.35.18.155"
    REDIS_PORT: int = 8568
    REDIS_PASS: str = (
        "SCltJIOZLDvcI6vy8SwaJ2EyziATp4jRsuHPHuw0LJAjhehiC1tChMiDHvnNc5VGQwJJIsnl6QNhcrHs"
    )


class ExtraSettings(BaseEnvSettings):
    BETTER_STACK_LOGS_TOKEN: str = "jNpXzQc5TR4C7aVyCnrmyQgp"


class Settings:
    server: ServerSettings = ServerSettings()
    redis: RedisSettings = RedisSettings()
    extra: ExtraSettings = ExtraSettings()


settings: Settings = Settings()
