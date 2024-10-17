from typing import TypeVar, Generic, Type
from models.mongo_base_entity import MongoBaseEntity
from database import MongoDB

T = TypeVar('T', bound=MongoBaseEntity)

class BaseRepository(Generic[T]):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(BaseRepository, cls).__new__(cls)
        return cls._instances[cls]

    def __init__(self, model_class: Type[T]):
        if not hasattr(self, 'initialized'):
            self.model_class = model_class
            self.db = MongoDB()
            self.collection_name = model_class.collection_name()
            self.initialized = True

    async def save(self, item: T) -> T:
        return await self.db.save(item)