from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base Task Schema
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False

# Schema for creating a Task
class TaskCreate(TaskBase):
    pass

# Schema for updating a Task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

# Schema for Task in response
class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True