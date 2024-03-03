from fastapi import APIRouter

from .communication.controllers import router as communication_router

router = APIRouter(prefix="/v1")

router.include_router(
    communication_router, prefix="/communication", tags=["communication"]
)
