from fastapi import HTTPException, status
from constants.error_codes import ErrorCode

class BadRequestException(HTTPException):
    def __init__(self, code: ErrorCode):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=code,
            headers={"WWW-Authenticate": "Bearer"},
        )
