from typing import List

from pydantic import BaseModel

from models.responses.friend_request_response import FriendRequestResponse


class FriendRequestsResponse(BaseModel):
    requests: List[FriendRequestResponse]