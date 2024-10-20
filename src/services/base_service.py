from typing import Generic, TypeVar, Type

from models.entities.mongo_base_entity import MongoBaseEntity

E = TypeVar('E', bound=MongoBaseEntity)

class BaseService(Generic[E]):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(BaseService, cls).__new__(cls)
        return cls._instances[cls]

    def __init__(self, model_class: Type[E]):
        if not hasattr(self, 'initialized'):
            self.model_class = model_class
            self.initialized = True