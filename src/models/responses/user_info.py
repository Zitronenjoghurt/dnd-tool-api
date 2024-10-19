from pydantic import BaseModel
from typing import List

from constants.permissions import GlobalPermission


class UserInfoPublic(BaseModel):
    username: str

class UserInfoPrivate(BaseModel):
    username: str
    email: str
    permissions: List[GlobalPermission]