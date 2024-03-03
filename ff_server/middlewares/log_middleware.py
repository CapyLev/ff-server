import logging
from typing import Callable, Awaitable

from fastapi import Request, Response

from config.logger import logger


async def log_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "client": request.client.host,
        "user_agent": request.headers.get("user-agent", "N/A"),
    }

    response = await call_next(request)

    log_level = logging.INFO

    if 300 < response.status_code < 500:
        log_level = logging.WARNING
    elif response.status_code >= 500:
        log_level = logging.ERROR

    log_dict.update(
        {
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", "N/A"),
        }
    )

    logger.log(log_level, "Sent response", extra=log_dict)

    return response
