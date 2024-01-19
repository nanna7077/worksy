from enum import Enum

AUTHENTICATION_HEADER = "Authorization"

class SystemEventType(Enum):
    ALERT = 0
    WARNING = 1
    ERROR = 2