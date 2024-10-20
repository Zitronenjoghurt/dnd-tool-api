from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from constants.error_codes import ErrorCode
from database import MongoDB, get_db
from errors.bad_request_error import BadRequestError
from errors.unauthorized_error import UnauthorizedError
from models.entities.registration_code import RegistrationCode
from models.entities.user import User
from models.responses.error_response import LoginErrorResponse, RegistrationErrorResponse
from models.responses.token import Token
from repositories.registration_code_repository import RegistrationCodeRepository, get_registration_code_repo
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
    registration_code: str,
    user_repo: UserRepository = Depends(get_user_repo),
    registration_code_repo: RegistrationCodeRepository = Depends(get_registration_code_repo),
):
    valid_registration_code = await registration_code_repo.fetch_valid_code(code=registration_code)
    if not isinstance(valid_registration_code, RegistrationCode):
        raise BadRequestError(ErrorCode.INVALID_REGISTRATION_CODE)

    existing_username = await user_repo.find_one(username=username)
    if isinstance(existing_username, User):
        raise BadRequestError(ErrorCode.USERNAME_TAKEN)

    existing_email = await user_repo.find_one(email=email)
    if isinstance(existing_email, User):
        raise BadRequestError(ErrorCode.EMAIL_TAKEN)

    valid_registration_code.used = True
    await registration_code_repo.save(valid_registration_code)

    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        registration_code=valid_registration_code.code
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
        raise UnauthorizedError(ErrorCode.INCORRECT_USERNAME_OR_PASSWORD)
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")