from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from constants.error_codes import ErrorCode
from database import get_db, MongoDB
from exceptions.bad_request_exception import BadRequestException
from exceptions.unauthorized_exception import UnauthorizedException
from models.entities.user import User
from models.responses.token import Token
from repositories.user_repository import UserRepository, get_user_repo
from security.authentication import authenticate_user, create_access_token
from security.password import hash_password

router = APIRouter()

@router.post("/register")
async def register_user(
        username: str,
        email: str,
        password: str,
        user_repo: UserRepository = Depends(get_user_repo)
):
    existing_username = await user_repo.find_one(username=username)
    if isinstance(existing_username, User):
        raise BadRequestException(ErrorCode.USERNAME_TAKEN)

    existing_email = await user_repo.find_one(email=email)
    if isinstance(existing_email, User):
        raise BadRequestException(ErrorCode.EMAIL_TAKEN)

    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )
    await user_repo.save(new_user)

@router.post("/token")
async def login(
        db: MongoDB = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException(ErrorCode.INCORRECT_USERNAME_OR_PASSWORD)
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")