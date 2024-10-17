from fastapi import APIRouter, Depends

from models.entities.user import User
from models.responses.user_info import UserInfoPublic, UserInfoPrivate
from security.authentication import get_current_user

router = APIRouter(prefix="/users")

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)) -> UserInfoPrivate:
    return current_user.get_private_info()