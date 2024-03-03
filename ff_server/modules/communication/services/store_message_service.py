from modules.communication.services.daos.message_dao import MessageDAO


class StoreMessageService:
    def __init__(self, message_dao: MessageDAO) -> None:
        self._message_dao = message_dao

    async def execute(
        self,
        room_uid: str,
        user_uid: str,
        content: str,
    ) -> None:
        await self._message_dao.add_msg_to_server_message(
            room_uid=room_uid,
            user_uid=user_uid,
            content=content,
        )
