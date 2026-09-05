from enum import Enum

class ChannelType(str, Enum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    PUSH = "PUSH"

class Priority(str, Enum):
    HIGH = "HIGH"
    LOW = "LOW"

class NotificationStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"