from pydantic import BaseModel

from constants.error_codes import ErrorCode, AuthenticationErrorCode, RegistrationErrorCode, LoginErrorCode


class GeneralErrorResponse(BaseModel):
    detail: ErrorCode

class AuthenticationErrorResponse(BaseModel):
    detail: AuthenticationErrorCode

class LoginErrorResponse(BaseModel):
    detail: LoginErrorCode

class RegistrationErrorResponse(BaseModel):
    detail: RegistrationErrorCode