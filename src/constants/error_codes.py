from enum import Enum
from typing import Literal


class ErrorCode(str, Enum):
    # Authentication
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"
    TOKEN_MISSING = "TOKEN_MISSING"

    # Friend request
    ALREADY_FRIENDS = "ALREADY_FRIENDS"
    ALREADY_SENT_REQUEST = "ALREADY_SENT_REQUEST"
    UNABLE_TO_BEFRIEND = "UNABLE_TO_BEFRIEND"

    USER_NOT_FOUND = "USER_NOT_FOUND"

    # Login
    INCORRECT_USERNAME_OR_PASSWORD = "INCORRECT_USERNAME_OR_PASSWORD"

    # Permission
    MISSING_PERMISSIONS = "MISSING_PERMISSIONS"

    # Registration
    EMAIL_TAKEN = "EMAIL_TAKEN"
    INVALID_REGISTRATION_CODE = "INVALID_REGISTRATION_CODE"
    USERNAME_TAKEN = "USERNAME_TAKEN"

AuthenticationErrorCode = Literal[
    ErrorCode.TOKEN_EXPIRED,
    ErrorCode.TOKEN_INVALID,
    ErrorCode.TOKEN_MISSING
]

FriendRequestErrorCode = Literal[
    ErrorCode.ALREADY_FRIENDS,
    ErrorCode.ALREADY_SENT_REQUEST,
    ErrorCode.UNABLE_TO_BEFRIEND,
]

LoginErrorCode = Literal[
    ErrorCode.INCORRECT_USERNAME_OR_PASSWORD,
]

PermissionErrorCode = Literal[
    ErrorCode.MISSING_PERMISSIONS,
]

RegistrationErrorCode = Literal[
    ErrorCode.EMAIL_TAKEN,
    ErrorCode.INVALID_REGISTRATION_CODE,
    ErrorCode.USERNAME_TAKEN
]