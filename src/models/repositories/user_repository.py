from models.base_repository import BaseRepository
from models.entities.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)