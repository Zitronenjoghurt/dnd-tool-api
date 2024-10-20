import datetime

from pydantic import BaseModel

from models.entities.registration_code import RegistrationCode


class RegistrationCodeResponse(BaseModel):
    code: str
    created_at: datetime.datetime
    used: bool

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_registration_code(code: RegistrationCode) -> 'RegistrationCodeResponse':
        return RegistrationCodeResponse(
            code=code.code,
            created_at=code.created_at,
            used=code.used,
        )