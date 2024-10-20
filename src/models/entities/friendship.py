import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel

from models.entities.mongo_base_entity import MongoBaseEntity


class FriendRequest(BaseModel):
    user_id: ObjectId
    created_at: datetime.datetime = datetime.datetime.now()

    class Config:
        arbitrary_types_allowed = True

class Friendship(MongoBaseEntity):
    user_ids: List[ObjectId]