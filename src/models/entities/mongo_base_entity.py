from typing import Optional, Type, Dict
from bson import ObjectId
from pydantic import BaseModel, Field

class MongoBaseEntity(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias='_id')

    @classmethod
    def collection_name(cls: Type['MongoBaseEntity']) -> str:
        return cls.__name__.lower()

    def to_dict(self, **kwargs) -> Dict:
        return self.model_dump(by_alias=True, exclude_none=True, **kwargs)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True