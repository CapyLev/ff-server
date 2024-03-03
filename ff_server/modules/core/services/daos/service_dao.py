from lib.redis_connection_manager import RedisConnectionManager


class ServiceDAO:
    async def redis_health_check(self) -> bool:
        async with RedisConnectionManager() as conn:
            return bool(await conn.ping())
