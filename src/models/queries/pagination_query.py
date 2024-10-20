from pydantic import BaseModel


class PaginationQuery(BaseModel):
    page: int = 1
    limit: int = 10

    def validate(self, max_limit: int = 100):
        self.page = max(0, self.page)
        self.limit = min(max(0, max_limit), self.limit)

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.limit