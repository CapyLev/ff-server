import ujson
from fastapi import WebSocket

from lib.redis_connection_manager import RedisConnectionManager
from lib.funcutils import get_timestamp_as_int, get_uuid_as_str


class MessageDAO:
    async def add_msg_to_server_message(
        self,
        room_uid: str,
        user_uid: str,
        content: str,
    ) -> None:
        msg_uid = await get_uuid_as_str()
        message_data = ujson.dumps(
            {
                "content": content,
                "timestamp": await get_timestamp_as_int(),
            }
        )

        async with RedisConnectionManager() as conn:
            await conn.set(f"user_msg:{room_uid}:{user_uid}:{msg_uid}", message_data)

    async def get_server_messages(self, room_uid: str) -> list:
        search_key = f"user_msg:{room_uid}:*"
        async with RedisConnectionManager() as conn:
            user_message_keys = await conn.keys(search_key)
            user_messages = await conn.mget(user_message_keys)

        return [msg for msg in user_messages if msg is not None]

    async def send_message_to_websocket(
        self, websocket: WebSocket, message: str
    ) -> None:
        await websocket.send_text(message)
