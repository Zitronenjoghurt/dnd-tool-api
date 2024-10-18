from pydantic import Field

from constants.global_permission_levels import GlobalPermissionLevel
from models.entities.mongo_base_entity import MongoBaseEntity
from models.responses.user_info import UserInfoPublic, UserInfoPrivate


class User(MongoBaseEntity):
    username: str
    email: str
    password_hash: str
    permission_level: int = Field(default=GlobalPermissionLevel.USER.value)

    def get_public_info(self) -> UserInfoPublic:
        return UserInfoPublic(username=self.username)

    def get_private_info(self) -> UserInfoPrivate:
        return UserInfoPrivate(
            username=self.username,
            email=self.email
        )

    def has_permission(self, permission_level: GlobalPermissionLevel) -> bool:
        return self.permission_level >= permission_level.value