from enum import EnumType, auto

class ErrorCode(EnumType):
    # Authentication
    INCORRECT_USERNAME_OR_PASSWORD = "INCORRECT_USERNAME_OR_PASSWORD"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"

    # Registration
    EMAIL_TAKEN = "EMAIL_TAKEN"
    USERNAME_TAKEN = "USERNAME_TAKEN"