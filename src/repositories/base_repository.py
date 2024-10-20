import asyncio
from typing import TypeVar, Generic, Type, Optional, List, Callable

from bson import ObjectId
from pydantic import BaseModel

from models.entities.mongo_base_entity import MongoBaseEntity
from database import MongoDB
from models.queries.pagination_query import PaginationQuery
from models.responses.paginated_entity_response import PaginatedEntityResponse

E = TypeVar('E', bound=MongoBaseEntity)
T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[E]):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(BaseRepository, cls).__new__(cls)
        return cls._instances[cls]

    def __init__(self, model_class: Type[E], db: MongoDB):
        if not hasattr(self, 'initialized'):
            self.model_class = model_class
            self.db = db
            self.collection_name = model_class.collection_name()
            self.initialized = True

    async def save(self, item: E) -> E:
        item_dict = item.to_dict()
        saved_dict = await self.db.save(self.collection_name, item_dict)
        return self.model_class.model_validate(saved_dict)

    async def save_many(self, items: List[E]) -> List[E]:
        save_tasks = [self.save(item) for item in items]
        return await asyncio.gather(*save_tasks)

    async def find(
        self,
        sort_key: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        **kwargs
    ) -> List[E]:
        results = await self.db.find(
            collection_name=self.collection_name,
            filter=kwargs,
            sort_key=sort_key,
            limit=limit,
            skip=skip
        )
        return [self.model_class.model_validate(result) for result in results if result is not None]

    async def find_paginated(self, query: PaginationQuery, data_transform: Callable[[E], T], **kwargs) -> PaginatedEntityResponse[T]:
        entities = await self.find(
            limit=query.limit,
            skip=query.skip,
            **kwargs
        )
        total = await self.count(**kwargs)
        entity_data = [data_transform(entity) for entity in entities]
        return PaginatedEntityResponse.create(query, total, entity_data)

    async def find_one(self, **kwargs) -> Optional[E]:
        results = await self.find(**kwargs)
        if len(results) == 0:
            return None
        return results[0]

    async def find_one_by_id(self, entity_id: str) -> Optional[E]:
        return await self.find_one(_id=ObjectId(entity_id))

    async def count(self, **kwargs) -> int:
        return await self.db.count(self.collection_name, kwargs)