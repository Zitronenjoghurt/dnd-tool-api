from typing import List

from fastapi import HTTPException, status
from pydantic import BaseModel

from constants.error_codes import PermissionErrorCode, ErrorCode
from constants.permissions import GlobalPermission

class GlobalPermissionErrorDetail(BaseModel):
    error_code: PermissionErrorCode
    permissions: List[GlobalPermission]

class GlobalPermissionError(HTTPException):
    def __init__(self, permissions: List[GlobalPermission], code: PermissionErrorCode = ErrorCode.MISSING_PERMISSIONS):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=GlobalPermissionErrorDetail(error_code=code, permissions=permissions).model_dump(),
            headers={"WWW-Authenticate": "Bearer"},
        )
