from typing import TypeVar, Generic, Type, Optional, List

from bson import ObjectId

from models.entities.mongo_base_entity import MongoBaseEntity
from database import MongoDB

T = TypeVar('T', bound=MongoBaseEntity)

class BaseRepository(Generic[T]):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(BaseRepository, cls).__new__(cls)
        return cls._instances[cls]

    def __init__(self, model_class: Type[T], db: MongoDB):
        if not hasattr(self, 'initialized'):
            self.model_class = model_class
            self.db = db
            self.collection_name = model_class.collection_name()
            self.initialized = True

    async def save(self, item: T) -> T:
        item_dict = item.to_dict()
        saved_dict = await self.db.save(self.collection_name, item_dict)
        return self.model_class.model_validate(saved_dict)

    async def find(
        self,
        sort_key: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        **kwargs
    ) -> List[T]:
        results = await self.db.find(
            collection_name=self.collection_name,
            filter=kwargs,
            sort_key=sort_key,
            limit=limit,
            skip=skip
        )
        return [self.model_class.model_validate(result) for result in results]

    async def find_one(self, **kwargs) -> Optional[T]:
        results = await self.find(**kwargs)
        if len(results) == 0:
            return None
        return results[0]

    async def find_one_by_id(self, entity_id: str) -> Optional[T]:
        return await self.find_one(_id=ObjectId(entity_id))