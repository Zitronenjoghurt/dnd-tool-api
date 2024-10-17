import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from exceptions.credentials_exception import CredentialsException
from models.entities.user import User
from repositories.user_repository import UserRepository
from security.password import verify_password

SECRET_KEY = os.environ.get('JWT_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(user_id: ObjectId, expires_delta: timedelta = None) -> str:
    to_encode = {"sub": str(user_id)}
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def authenticate_user(username: str, password: str) -> Optional[User]:
    user = await UserRepository().find_one(username=username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise CredentialsException()
    except jwt.ExpiredSignatureError:
        raise CredentialsException("Token expired")
    except jwt.PyJWTError:
        raise CredentialsException("Invalid token")
    user = await UserRepository().find_one_by_id(user_id)
    if user is None:
        raise CredentialsException()
    return user