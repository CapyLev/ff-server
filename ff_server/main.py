import uvicorn

from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from middlewares import log_middleware
from modules import router


def start_application() -> FastAPI:
    application = FastAPI(
        title=settings.server.NAME,
        version=settings.server.VERSION,
        **settings.server.fastapi_kwargs,
    )

    setup_settings(application)

    return application


def setup_settings(application: FastAPI) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(prefix="/api", router=router)
    application.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)


app: FastAPI = start_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.server.HOST,
        port=settings.server.PORT,
        workers=settings.server.WORKERS,
        reload=settings.server.RELOAD,
        log_level=settings.server.LOG_LEVEL,
        timeout_keep_alive=settings.server.KEEPALIVE,
    )
