from typing import Dict

from lib.funcutils import get_uuid_as_str
from modules.communication.services.daos import RoomsDAO, CreateRoomRequestData


class CreateRoomService:
    def __init__(
        self,
        rooms_dao: RoomsDAO,
    ) -> None:
        self._rooms_dao = rooms_dao

    async def execute(self, create_data: CreateRoomRequestData) -> Dict[str, str]:
        room_uid = await get_uuid_as_str()

        await self._rooms_dao.create_room(
            room_uid=room_uid,
            room_info=create_data,
        )

        return {
            "room_uid": room_uid,
            "room_name": create_data.room_name,
            "admin_uid": create_data.admin_uid,
            "admin_name": create_data.admin_name,
        }
