from pydantic import Field

from models.queries.pagination_query import PaginationQuery


class RegistrationCodeQuery(PaginationQuery):
    unused: bool = Field(default=True, description="If only unused registration codes should be fetched")