from typing import List

from pydantic import BaseModel


class GeneratedRegistrationCodesResponse(BaseModel):
    codes: List[str]