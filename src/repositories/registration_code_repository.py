from fastapi.params import Depends

from database import MongoDB, get_db
from models.entities.registration_code import RegistrationCode
from repositories.base_repository import BaseRepository

class RegistrationCodeRepository(BaseRepository[RegistrationCode]):
    def __init__(self, db: MongoDB):
        super().__init__(RegistrationCode, db)

async def get_registration_code_repo(db: MongoDB = Depends(get_db)):
    return RegistrationCodeRepository(db)