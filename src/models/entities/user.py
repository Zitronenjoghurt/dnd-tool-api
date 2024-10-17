from models.entities.mongo_base_entity import MongoBaseEntity
from models.responses.user_info import UserInfoPublic, UserInfoPrivate


class User(MongoBaseEntity):
    username: str
    email: str
    password_hash: str

    def get_public_info(self) -> UserInfoPublic:
        return UserInfoPublic(username=self.username)

    def get_private_info(self) -> UserInfoPrivate:
        return UserInfoPrivate(
            username=self.username,
            email=self.email
        )