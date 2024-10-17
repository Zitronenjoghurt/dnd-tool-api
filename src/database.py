import os
from typing import Optional, List, Dict, Any
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient

from models.entities.mongo_base_entity import MongoBaseEntity

class MongoDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.hostname = os.getenv('MONGO_HOSTNAME')
            self.port = os.getenv('MONGO_PORT')
            self.database_name = os.getenv('MONGO_DATABASE')
            self.username = os.getenv('MONGO_USERNAME')
            self.password = os.getenv('MONGO_PASSWORD')
            self.auth_source = os.getenv('MONGO_AUTH_SOURCE')

            self.connection_string = self._build_connection_string()
            self.async_client = AsyncIOMotorClient(self.connection_string)
            self.async_db = self.async_client.get_database(self.database_name)
            self.initialized = True

    def _build_connection_string(self) -> str:
        auth = ""
        if self.username and self.password:
            auth = f"{quote_plus(self.username)}:{quote_plus(self.password)}@"

        options = [
            f"authSource={self.auth_source}",
        ]

        return f"mongodb://{auth}{self.hostname}:{self.port}/{self.database_name}?{'&'.join(options)}"

    async def save(self, collection_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        collection = self.async_db[collection_name]
        if '_id' in item and item['_id']:
            # Update existing document
            await collection.update_one({'_id': item['_id']}, {'$set': item})
        else:
            # Insert new document
            result = await collection.insert_one(item)
            item['_id'] = result.inserted_id
        return item

    async def find(
        self,
        collection_name: str,
        filter: Optional[dict] = None,
        sort_key: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[dict]:
        collection = self.async_db[collection_name]

        query = collection.find(filter or {})

        if sort_key:
            query = query.sort(sort_key)

        if skip is not None:
            query = query.skip(skip)

        if limit is not None:
            query = query.limit(limit)

        return await query.to_list(length=None)