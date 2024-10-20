from typing import Optional

from fastapi.params import Depends

from database import MongoDB, get_db
from repositories.base_repository import BaseRepository
from models.entities.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self, db: MongoDB):
        super().__init__(User, db)

    async def save(self, item: User) -> User:
        item.username = item.username.lower()
        return await super().save(item)

    async def find_by_username(self, username: str) -> Optional[User]:
        username = username.lower()
        return await self.find_one(username=username)

async def get_user_repo(db: MongoDB = Depends(get_db)):
    return UserRepository(db)