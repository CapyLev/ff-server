from typing import Dict, List, Tuple, TypeVar
from dataclasses import dataclass

from fastapi import WebSocket

from lib.funcutils import get_timestamp_as_int


@dataclass(frozen=True, slots=True)
class WebSocketPullData:
    ws: WebSocket
    timestamp: int


K = TypeVar("K", bound=Tuple[str, str])


class WebSocketPullManager:
    def __init__(self) -> None:
        self.active_connections: Dict[K, WebSocketPullData] = {}

    async def _get_key(
        self,
        room_uid: str,
        user_uid: str,
    ) -> K:
        return room_uid, user_uid

    async def add_connection_to_pull(
        self,
        room_uid: str,
        user_uid: str,
        ws: WebSocket,
    ) -> None:
        key = await self._get_key(room_uid, user_uid)
        timestamp = await get_timestamp_as_int()
        self.active_connections[key] = WebSocketPullData(ws, timestamp)

    async def remove_connection_from_pull(
        self,
        room_uid: str,
        user_uid: str,
    ) -> None:
        key = await self._get_key(room_uid, user_uid)
        if key in self.active_connections:
            del self.active_connections[key]

    async def get_active_connections(
        self,
        room_uid: str,
    ) -> List[WebSocketPullData]:
        connections = []
        for (s_id, u_id), data in self.active_connections.items():
            if s_id == room_uid:
                connections.append(data)

        return connections


websocket_pull_manager: WebSocketPullManager = WebSocketPullManager()
