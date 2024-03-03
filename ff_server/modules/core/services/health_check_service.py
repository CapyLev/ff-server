import time

from modules.core.services.daos.service_dao import ServiceDAO


class HealthCheckService:
    class HealthCheckServiceException(Exception):
        pass

    class RedisIsDeadBroException(HealthCheckServiceException):
        pass

    def __init__(
        self,
        service_dao: ServiceDAO,
    ) -> None:
        self._service_dao = service_dao

    async def execute(self) -> int:
        s_time = time.perf_counter_ns()

        if not await self._service_dao.redis_health_check():
            raise self.RedisIsDeadBroException

        e_time = time.perf_counter_ns()

        return int(e_time - s_time)
