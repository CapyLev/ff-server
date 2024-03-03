from fastapi import WebSocket

from modules.communication.services.daos.message_dao import MessageDAO


class SendMessagesOnConnectService:
    def __init__(
        self,
        message_dao: MessageDAO,
    ) -> None:
        self._message_dao = message_dao

    async def execute(
        self,
        ws: WebSocket,
        room_uid: str,
    ) -> None:
        server_messages = await self._message_dao.get_server_messages(room_uid)

        for message in server_messages:
            await self._message_dao.send_message_to_websocket(
                websocket=ws,
                message=message,
            )
