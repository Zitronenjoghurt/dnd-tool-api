import os

from constants.permissions import GlobalPermission
from database import get_db
from models.entities.user import User
from repositories.user_repository import UserRepository
from security.password import hash_password, verify_password

async def create_super_user():
    username = os.getenv('SUPERUSER_NAME')
    password = os.getenv('SUPERUSER_PASSWORD')

    if not isinstance(username, str) or not isinstance(password, str):
        raise RuntimeError('Missing super user credentials')

    password_hash = hash_password(password)

    db = await get_db()
    user_repo = UserRepository(db)
    existing_user = await user_repo.find_by_username(username)
    if isinstance(existing_user, User):
        if not verify_password(password, existing_user.password_hash):
            raise RuntimeError('Super user password has changed')
        return

    user = User(
        username=username,
        password_hash=password_hash,
        email='',
        registration_code='',
        accepts_friend_requests=False
    )
    user.add_global_permission(GlobalPermission.SUPER_USER)
    await user_repo.save(user)