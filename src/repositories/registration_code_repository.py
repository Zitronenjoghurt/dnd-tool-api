from typing import Optional

from fastapi.params import Depends

from database import MongoDB, get_db
from models.entities.registration_code import RegistrationCode
from repositories.base_repository import BaseRepository

class RegistrationCodeRepository(BaseRepository[RegistrationCode]):
    def __init__(self, db: MongoDB):
        super().__init__(RegistrationCode, db)

    async def fetch_valid_code(self, code: str) -> Optional[RegistrationCode]:
        registration_code = await self.find_one(code=code)
        if not isinstance(registration_code, RegistrationCode):
            return None
        return registration_code if not registration_code.used else None

async def get_registration_code_repo(db: MongoDB = Depends(get_db)):
    return RegistrationCodeRepository(db)