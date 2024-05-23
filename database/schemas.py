from datetime import datetime

from pydantic import BaseModel, constr
from typing import Optional


class TaskSchema(BaseModel):
    id: int
    title: constr(min_length=1)
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskCreateSchema(BaseModel):
    title: constr(min_length=1)
    description: Optional[str] = None


class TaskUpdateSchema(BaseModel):
    title: Optional[constr(min_length=1)] = None
    description: Optional[str] = None


class TaskDeleteSchema(BaseModel):
    message: Optional[str] = 'Task deleted successfully'

