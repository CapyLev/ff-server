import time
import uuid


async def get_uuid_as_str() -> str:
    return str(uuid.uuid4())


async def get_timestamp_as_int() -> int:
    return int(time.time())
