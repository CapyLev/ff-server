from fastapi import APIRouter

from .communication.controllers import router as communication_router
from .core.controller import router as core_router


router = APIRouter(prefix="/v1")

router.include_router(communication_router, prefix="/communication", tags=["communication"])
router.include_router(core_router, prefix="/core", tags=["core", "system"])

