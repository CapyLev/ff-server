from typing import Dict

from fastapi import APIRouter

from modules.core.services.daos.service_dao import ServiceDAO
from modules.core.services.health_check_service import HealthCheckService

router = APIRouter()


@router.get('')
async def health_check() -> Dict[str, str]:
    service: HealthCheckService = HealthCheckService(service_dao=ServiceDAO())
    time_to_get_result = await service.execute()
    return {
        "time_to_get_result": time_to_get_result,
        "SERVER": "Server is up and running!",
        "REDIS": "Redis is up and running!"
    }
