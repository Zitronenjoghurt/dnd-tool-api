from datetime import datetime

from models.responses.user_info import UserInfoPublic


class FriendResponse(UserInfoPublic):
    since: datetime