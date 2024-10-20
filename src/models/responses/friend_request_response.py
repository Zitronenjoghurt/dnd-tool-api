from datetime import datetime

from pydantic import BaseModel

from models.responses.user_info import UserInfoPublic


class FriendRequestResponse(BaseModel):
    user_info: UserInfoPublic
    created_at: datetime