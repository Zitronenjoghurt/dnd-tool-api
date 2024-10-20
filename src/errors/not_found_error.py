from fastapi import HTTPException, status

from constants.error_codes import ErrorCode


class NotFoundError(HTTPException):
    def __init__(self, code: ErrorCode):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=code.value,
            headers={"WWW-Authenticate": "Bearer"},
        )
