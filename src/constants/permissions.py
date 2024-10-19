from enum import Enum

class GlobalPermission(str, Enum):
    SUPER_USER = "SUPER_USER"
    MANAGE_REGISTRATION_CODES = "MANAGE_REGISTRATION_CODES"