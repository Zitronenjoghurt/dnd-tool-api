from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from constants.error_codes import ErrorCode
from database import MongoDB, get_db
from exceptions.bad_request_exception import BadRequestException
from exceptions.unauthorized_exception import UnauthorizedException
from models.entities.user import User
from models.responses.error_response import LoginErrorResponse, RegistrationErrorResponse
from models.responses.token import Token
from repositories.user_repository import UserRepository, get_user_repo
from security.authentication import authenticate_user, create_access_token
from security.password import hash_password

router = APIRouter(tags=["Authentication"])

@router.post(
    "/register",
    summary="Register with your credentials which you can then use to fetch a JWT access token",
    response_description="Empty response",
    status_code=status.HTTP_200_OK,
    responses={401: {"model": RegistrationErrorResponse}}
)
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

@router.post(
    "/token",
    summary="Login with your credentials to fetch a valid JWT token",
    response_model=Token,
    response_description="Your JWT token including the type of the token",
    status_code=status.HTTP_200_OK,
    responses={401: {"model": LoginErrorResponse}}
)
async def login(
    db: MongoDB = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not isinstance(user, User):
        raise UnauthorizedException(ErrorCode.INCORRECT_USERNAME_OR_PASSWORD)
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")