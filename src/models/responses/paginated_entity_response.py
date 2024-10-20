from typing import TypeVar, List, Callable

import math
from pydantic import BaseModel
from typing_extensions import Generic

from models.queries.pagination_query import PaginationQuery

T = TypeVar('T', bound=BaseModel)

class PaginatedEntityResponse(BaseModel, Generic[T]):
    page: int
    count: int
    limit: int
    total: int
    max_pages: int
    entities: List[T]

    @staticmethod
    def create(pagination: PaginationQuery, total: int, entities: List[T]) -> 'PaginatedEntityResponse':
        count = len(entities)
        max_pages = math.ceil(total / pagination.limit)
        return PaginatedEntityResponse(
            page=pagination.page,
            count=count,
            limit=pagination.limit,
            total=total,
            max_pages=max_pages,
            entities=entities
        )