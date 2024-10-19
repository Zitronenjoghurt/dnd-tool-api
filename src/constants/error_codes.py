from enum import Enum
from typing import Literal


class ErrorCode(Enum):
    # Authentication
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"
    TOKEN_MISSING = "TOKEN_MISSING"

    # Login
    INCORRECT_USERNAME_OR_PASSWORD = "INCORRECT_USERNAME_OR_PASSWORD"

    # Registration
    EMAIL_TAKEN = "EMAIL_TAKEN"
    USERNAME_TAKEN = "USERNAME_TAKEN"

AuthenticationErrorCode = Literal[
    ErrorCode.TOKEN_EXPIRED,
    ErrorCode.TOKEN_INVALID,
    ErrorCode.TOKEN_MISSING
]

LoginErrorCode = Literal[
    ErrorCode.INCORRECT_USERNAME_OR_PASSWORD,
]

RegistrationErrorCode = Literal[
    ErrorCode.EMAIL_TAKEN,
    ErrorCode.USERNAME_TAKEN
]