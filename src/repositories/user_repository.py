from typing import Optional, List

from bson import ObjectId
from fastapi.params import Depends

from database import MongoDB, get_db
from models.entities.friendship import Friendship
from models.responses.friend_response import FriendResponse
from models.responses.paginated_entity_response import PaginatedEntityResponse
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

    async def get_friend_list(self, user: User) -> List[FriendResponse]:
        pipeline = [
            {"$match": {"user_ids": user.id}},
            {"$unwind": "$user_ids"},
            # Filter out current user's ID
            {"$match": {"user_ids": {"$ne": user.id}}},
            # Find user entries of all friends
            {"$lookup": {
                "from": User.collection_name(),
                "localField": "user_ids",
                "foreignField": "_id",
                "as": "friend"
            }},
            {"$unwind": "$friend"},
            # Only return the required fields
            {"$project": {
                "_id": 0,
                # Makes sure to include the friend's username
                "username": "$friend.username",
                # Renames the initial friendships created_at to since
                "since": "$created_at"
            }}
        ]

        cursor = self.db.get_collection(Friendship.collection_name()).aggregate(pipeline)
        friendships = await cursor.to_list()
        friend_responses = [FriendResponse.model_validate(friendship) for friendship in friendships]
        return friend_responses

async def get_user_repo(db: MongoDB = Depends(get_db)):
    return UserRepository(db)