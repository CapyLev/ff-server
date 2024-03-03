from redis.asyncio import Redis

from config import settings


class RedisConnectionManager:
    def __init__(self) -> None:
        self.connection = None

    async def __aenter__(self):
        self.connection = await self._get_redis_session_by_type()
        return self.connection

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.connection.aclose()

    async def _get_redis_session_by_type(
        self,
    ) -> Redis:
        return await Redis(
            host=settings.redis.REDIS_HOST,
            port=settings.redis.REDIS_PORT,
            password=settings.redis.REDIS_PASS,
            encoding="utf-8",
            decode_responses=True,
        )
