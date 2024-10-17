from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
            headers={"WWW-Authenticate": "Bearer"},
        )

    existing_email = await UserRepository().find_one(email=email)
    if isinstance(existing_email, User):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-Mail already in use",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")