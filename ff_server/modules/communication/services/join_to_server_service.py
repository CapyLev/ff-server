from modules.communication.services.daos import RoomsDAO


class JoinToServerService:
    class JoinToServerServiceException(Exception):
        pass

    class RoomNotFoundException(JoinToServerServiceException):
        pass

    class InvalidPasswordException(JoinToServerServiceException):
        pass

    def __init__(
        self,
        rooms_dao: RoomsDAO,
    ) -> None:
        self._rooms_dao = rooms_dao

    async def execute(
        self,
        room_uid: str,
        user_uid: str,
        user_name: str,
        password: str,
    ) -> None:
        if not await self._rooms_dao.check_if_room_exist(room_uid):
            raise self.RoomNotFoundException

        if not await self._rooms_dao.check_if_password_valid(
            room_uid=room_uid,
            provided_password=password,
        ):
            raise self.InvalidPasswordException

        await self._rooms_dao.add_user_to_room(
            room_uid=room_uid,
            user_uid=user_uid,
            user_name=user_name,
        )
