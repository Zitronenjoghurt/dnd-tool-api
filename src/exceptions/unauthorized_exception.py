from fastapi import HTTPException, status

from constants.error_codes import ErrorCode


class UnauthorizedException(HTTPException):
    def __init__(self, code: ErrorCode):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=code.value,
            headers={"WWW-Authenticate": "Bearer"},
        )
