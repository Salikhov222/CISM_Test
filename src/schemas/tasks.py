from enum import Enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ERROR = 'error'

class Task(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")

    model_config = ConfigDict(from_attributes=True)