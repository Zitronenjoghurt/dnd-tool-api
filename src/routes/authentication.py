from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from constants.error_codes import ErrorCode
from exceptions.bad_request_exception import BadRequestException
from exceptions.unauthorized_exception import UnauthorizedException
from models.entities.user import User
from models.responses.token import Token
from repositories.user_repository import UserRepository
from security.authentication import authenticate_user, create_access_token
from security.password import hash_password

router = APIRouter()

@router.post("/register")
async def register_user(username: str, email: str, password: str):
    existing_username = await UserRepository().find_one(username=username)
    if isinstance(existing_username, User):
        raise BadRequestException(ErrorCode.USERNAME_TAKEN)

    existing_email = await UserRepository().find_one(email=email)
    if isinstance(existing_email, User):
        raise BadRequestException(ErrorCode.EMAIL_TAKEN)

    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )
    await UserRepository().save(new_user)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException(ErrorCode.INCORRECT_USERNAME_OR_PASSWORD)
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")