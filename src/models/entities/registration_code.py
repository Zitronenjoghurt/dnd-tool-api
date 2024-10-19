import datetime
import uuid
from typing import Optional

from bson import ObjectId

from models.entities.mongo_base_entity import MongoBaseEntity
from models.entities.user import User


class RegistrationCode(MongoBaseEntity):
    code: str
    created_by: Optional[ObjectId] = None
    created_at: datetime = datetime.datetime.now()
    used: bool = False

    @staticmethod
    def generate(creator: User) -> 'RegistrationCode':
        random_uuid = str(uuid.uuid4()).replace('-', '')
        return RegistrationCode(code=random_uuid, created_by=creator.id)