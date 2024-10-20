from typing import Optional, List, Dict, Any
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from config import settings

class MongoDB:
    def __init__(self):
        connection_string = build_connection_string()

        self.client = AsyncIOMotorClient(connection_string, maxPoolSize=10, minPoolSize=1)
        self.db = self.client[settings.MONGO_DATABASE]

        self.client_sync = MongoClient(connection_string)
        self.db_sync = self.client_sync[settings.MONGO_DATABASE]

    def clear(self) -> None:
        collection_names = self.db_sync.list_collection_names()
        for collection_name in collection_names:
            self.db_sync.drop_collection(collection_name)

    async def save(self, collection_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        collection = self.db[collection_name]
        if '_id' in item and item['_id']:
            await collection.update_one({'_id': item['_id']}, {'$set': item})
        else:
            result = await collection.insert_one(item)
            item['_id'] = result.inserted_id
        return item

    async def create_unique_index(self, collection_name: str, field_name: str):
        collection = self.db[collection_name]
        await collection.create_index(field_name, unique=True)

    async def count(self, collection_name: str, filter: Optional[dict] = None) -> int:
        collection = self.db[collection_name]
        if filter is None:
            return await collection.estimated_document_count()
        else:
            return await collection.count_documents(filter or {})

    async def find(
        self,
        collection_name: str,
        filter: Optional[dict] = None,
        sort_key: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        additional_filters: Optional[Dict[str, Any]] = None,
    ) -> List[dict]:
        collection = self.db[collection_name]

        combined_filter = filter or {}
        if isinstance(additional_filters, dict):
            combined_filter.update(additional_filters)

        query = collection.find(combined_filter)

        if sort_key:
            query = query.sort(sort_key)

        if skip is not None:
            query = query.skip(skip)

        if limit is not None:
            query = query.limit(limit)

        return await query.to_list(length=None)

def build_connection_string() -> str:
    auth = ""
    if settings.MONGO_USERNAME and settings.MONGO_PASSWORD:
        auth = f"{quote_plus(settings.MONGO_USERNAME)}:{quote_plus(settings.MONGO_PASSWORD)}@"

    return f"mongodb://{auth}{settings.MONGO_HOSTNAME}:{settings.MONGO_PORT}/{settings.MONGO_DATABASE}?authSource={settings.MONGO_AUTH_SOURCE}"

mongodb = MongoDB()

async def get_db():
    return mongodb
