import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId
from fastapi import Depends

from config import settings
from constants.error_codes import ErrorCode
from database import MongoDB, get_db
from exceptions.unauthorized_exception import UnauthorizedException
from models.entities.user import User
from repositories.user_repository import UserRepository
from security.password import verify_password

def create_access_token(user_id: ObjectId, expires_delta: timedelta = None) -> str:
    to_encode = {"sub": str(user_id)}
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.JWT_TOKEN_EXP_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_KEY, algorithm=settings.JWT_ALGORITHM)

async def authenticate_user(db: MongoDB, username: str, password: str) -> Optional[User]:
    user = await UserRepository(db).find_one(username=username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

async def get_current_user(db: MongoDB = Depends(get_db), token: str = Depends(settings.OAUTH2_SCHEME)) -> User:
    if not isinstance(token, str):
        raise UnauthorizedException(ErrorCode.TOKEN_MISSING)
    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException(ErrorCode.TOKEN_INVALID)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException(ErrorCode.TOKEN_EXPIRED)
    except jwt.PyJWTError:
        raise UnauthorizedException(ErrorCode.TOKEN_INVALID)

    user = await UserRepository(db).find_one_by_id(user_id)
    if user is None:
        raise UnauthorizedException(ErrorCode.TOKEN_INVALID)
    return user