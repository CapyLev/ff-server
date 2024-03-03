from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from fastapi.responses import UJSONResponse

from modules.communication.services import (
    CreateRoomService,
    CreateRoomRequestData,
    JoinToServerService,
)
from modules.communication.manager.connection_manager import ConnectionManager
from modules.communication.services.daos import RoomsDAO

router = APIRouter()


@router.post(
    "/room", status_code=status.HTTP_201_CREATED, response_model=Dict[str, str]
)
async def create_room(
    create_room_request_data: CreateRoomRequestData,
) -> Dict[str, str]:
    create_room_service = CreateRoomService(rooms_dao=RoomsDAO())
    result = await create_room_service.execute(create_room_request_data)
    return result


@router.websocket("/ws/{room_uid}/{user_uid}/{user_name}/{password}")
async def chat_communication(
    websocket: WebSocket,
    room_uid: str,
    user_uid: str,
    user_name: str,
    password: str,
):
    join_to_server_service = JoinToServerService(rooms_dao=RoomsDAO())
    try:
        await join_to_server_service.execute(
            room_uid=room_uid,
            user_uid=user_uid,
            user_name=user_name,
            password=password,
        )
    except join_to_server_service.RoomNotFoundException:
        return UJSONResponse({"error": "Room not found"}, status_code=404)

    await ConnectionManager.connect(
        websocket=websocket,
        room_uid=room_uid,
        user_uid=user_uid,
    )

    try:
        while True:
            msg = await websocket.receive_text()
            await ConnectionManager.broadcast(
                room_uid=room_uid,
                user_uid=user_uid,
                message_content=msg,
            )
    except WebSocketDisconnect:
        await ConnectionManager.disconnect(
            room_uid=room_uid,
            user_id=user_uid,
        )
        # TODO: если чел админ то удалить сервер, если нет то кикнуть его из user_server редиса
