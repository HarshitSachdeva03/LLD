from enum import Enum
from pydantic import BaseModel, Field
import time
import uuid

class JobState(str, Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Job(BaseModel):
    # Field(default_factory=...) auto-generates values when a job is created
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    priority: int = Field(..., description="Lower number means higher priority (0 is highest)")
    payload: str = Field(..., description="The actual task data or name")
    state: JobState = Field(default=JobState.PENDING)
    created_at: float = Field(default_factory=time.time)
    
    # Custom comparison to allow Python's heapq to sort Job objects directly
    def __lt__(self, other: "Job"):
        # Primary sort: Priority (lower integer = higher priority)
        if self.priority != other.priority:
            return self.priority < other.priority
        # Secondary sort: FIFO (if priorities are equal, older jobs run first)
        return self.created_at < other.created_at
