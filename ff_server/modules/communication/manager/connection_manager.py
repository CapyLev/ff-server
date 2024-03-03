from fastapi import WebSocket

from .websocket_pull_manager import websocket_pull_manager
from ..services import SendMessagesOnConnectService
from ..services.daos.message_dao import MessageDAO
from ..services.store_message_service import StoreMessageService


class ConnectionManager:
    @staticmethod
    async def connect(
        websocket: WebSocket,
        room_uid: str,
        user_uid: str,
    ):
        await websocket_pull_manager.add_connection_to_pull(
            ws=websocket,
            room_uid=room_uid,
            user_uid=user_uid,
        )
        await websocket.accept()

        send_message_on_connect_service = SendMessagesOnConnectService(
            message_dao=MessageDAO(),
        )
        await send_message_on_connect_service.execute(ws=websocket, room_uid=room_uid)

    @staticmethod
    async def disconnect(
        room_uid: str,
        user_id: str,
    ):
        await websocket_pull_manager.remove_connection_from_pull(room_uid, user_id)

    @staticmethod
    async def broadcast(
        room_uid: str,
        user_uid: str,
        message_content: str,
    ):
        active_connections = await websocket_pull_manager.get_active_connections(
            room_uid=room_uid,
        )

        store_message_service = StoreMessageService(message_dao=MessageDAO())
        await store_message_service.execute(
            room_uid=room_uid,
            user_uid=user_uid,
            content=message_content,
        )

        for pull_data in active_connections:
            ws = pull_data.ws
            await ws.send_text(message_content)
