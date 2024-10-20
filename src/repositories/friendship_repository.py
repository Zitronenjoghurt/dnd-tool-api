from typing import List, Optional

from bson import ObjectId
from fastapi import Depends

from database import MongoDB, get_db
from models.entities.friendship import Friendship
from repositories.base_repository import BaseRepository


class FriendshipRepository(BaseRepository[Friendship]):
    def __init__(self, db: MongoDB):
        super().__init__(Friendship, db)

    async def find_by_including_user_ids(self, user_ids: List[ObjectId]) -> Optional[Friendship]:
        additional_filters = {"user_ids": {"$in": user_ids}}
        friendship = await self.find_one(additional_filters=additional_filters)
        return friendship

async def get_friendship_repo(db: MongoDB = Depends(get_db)):
    return FriendshipRepository(db)