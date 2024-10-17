from pydantic import BaseModel

class UserInfoPublic(BaseModel):
    username: str

class UserInfoPrivate(BaseModel):
    username: str
    email: str