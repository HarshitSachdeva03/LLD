from pydantic import BaseModel, Field
import uuid
import time
from app.domain.enums import Priority, ChannelType, NotificationStatus

class NotificationRequest(BaseModel):    
    id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = Field(..., description="Target Recipient ID")
    message:str = Field(..., min_length=1, max_length=1000)
    channels:list[ChannelType] = Field(..., min_length=1)
    priority:Priority = Priority.LOW
    status:NotificationStatus = NotificationStatus.PENDING
    created_at:float = Field(default_factory=time.time)

