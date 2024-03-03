import logging
import sys

from logtail import LogtailHandler

from .config import settings


logger = logging.getLogger()

formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("logs/communication.log")
better_stack_handler = LogtailHandler(
    source_token=settings.extra.BETTER_STACK_LOGS_TOKEN
)

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers = [stream_handler, file_handler, better_stack_handler]

logger.setLevel(logging.INFO)
