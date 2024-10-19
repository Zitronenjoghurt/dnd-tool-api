from typing import TypeVar, List, Callable

from pydantic import BaseModel
from typing_extensions import Generic

T = TypeVar('T', bound=BaseModel)

class PaginatedEntityResponse(BaseModel, Generic[T]):
    page: int
    limit: int
    entities: List[T]