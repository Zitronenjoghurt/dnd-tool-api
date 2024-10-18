from typing import Optional

from fastapi.params import Depends

from database import MongoDB, get_db
from repositories.base_repository import BaseRepository
from models.entities.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self, db: MongoDB):
        super().__init__(User, db)

def get_user_repo(db: MongoDB = Depends(get_db)):
    return UserRepository(db)