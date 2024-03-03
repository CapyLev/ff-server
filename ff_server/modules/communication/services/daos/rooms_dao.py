import ujson
from pydantic import BaseModel

import config.const
from lib.redis_connection_manager import RedisConnectionManager


class CreateRoomRequestData(BaseModel):
    admin_uid: str
    admin_name: str
    room_name: str
    password: str


class RoomsDAO:
    async def create_room(
        self,
        room_uid: str,
        room_info: CreateRoomRequestData,
    ) -> None:
        mapping_room_info = {
            "admin_uid": room_info.admin_uid,
            "admin_name": room_info.admin_name,
            "room_name": room_info.room_name,
            "password": room_info.password,
        }

        async with RedisConnectionManager() as conn:
            await conn.hmset(f"room:{room_uid}", mapping_room_info)
            await conn.expire(f"room:{room_uid}", config.const.DAY)

    async def add_user_to_room(
        self,
        room_uid: str,
        user_uid: str,
        user_name: str,
    ) -> None:
        user_info = ujson.dumps(
            {
                "user_uid": user_uid,
                "user_name": user_name,
            }
        )

        async with RedisConnectionManager() as conn:
            await conn.sadd(f"room_users:{room_uid}", user_info)
            await conn.set(f"user_room:{user_uid}", room_uid, ex=config.const.DAY)

    async def remove_user_from_room(self, user_uid: str) -> None:
        async with RedisConnectionManager() as conn:
            room_uid = await conn.get(f"user_room:{user_uid}")
            if room_uid:
                await conn.srem(
                    f"room_users:{room_uid}", ujson.dumps({"user_uid": user_uid})
                )
                await conn.delete(f"user_room:{user_uid}")

    async def check_if_room_exist(self, room_uid: str) -> bool:
        async with RedisConnectionManager() as conn:
            return await conn.exists(f"room:{room_uid}")

    async def check_if_password_valid(
        self,
        room_uid: str,
        provided_password: str,
    ) -> bool:
        async with RedisConnectionManager() as conn:
            stored_password = await conn.hget(f"room:{room_uid}", "password")
            return stored_password == provided_password
