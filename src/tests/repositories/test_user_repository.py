import pytest
from starlette.testclient import TestClient

from constants.global_permission_levels import GlobalPermissionLevel
from database import get_db
from models.entities.user import User
from repositories.user_repository import UserRepository

# ToDo: Fix asynchronous tests
#@pytest.mark.asyncio
#async def test_save_user(client: TestClient):
#    db = await get_db()
#    user_repository = UserRepository(db)
#
#    user = User(username='test_save_user', email='test_save_user@example.com', password_hash='')
#    await user_repository.save(user)
#
#    user_retrieved = user_repository.find_one(username='test_save_user')
#    assert isinstance(user_retrieved, User)
#    assert user_retrieved.username == 'test_save_user'
#    assert user_retrieved.email == 'test_save_user@example.com'
#    assert user_retrieved.password_hash == ''
#    assert user_retrieved.permission_level == GlobalPermissionLevel.USER.value
#
#    user_retrieved.username = 'test_save_user_changed'
#    await user_repository.save(user_retrieved)
#
#    user_before_change = user_repository.find_one(username='test_save_user')
#    assert user_before_change is None
#
#    user_changed = user_repository.find_one(username='test_save_user_changed')
#    assert isinstance(user_changed, User)
#    assert user_changed.username == 'test_save_user_changed'
#    assert user_changed.email == 'test_save_user@example.com'
#    assert user_changed.password_hash == ''
#    assert user_changed.permission_level == GlobalPermissionLevel.USER.value