from typing import Optional, Type, Dict
from bson import ObjectId
from pydantic import Field
from pydantic.v1 import BaseModel
from pydantic_core import core_schema

class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.to_string_ser_schema(),
        )

class MongoBaseEntity(BaseModel):
    id: Optional[PydanticObjectId] = Field(default_factory=PydanticObjectId, alias='_id')

    @classmethod
    def collection_name(cls: Type['MongoBaseEntity']) -> str:
        return cls.__name__.lower()

    def to_dict(self, **kwargs) -> Dict:
        return self.dict(by_alias=True, exclude={'id'}, exclude_none=True, **kwargs)