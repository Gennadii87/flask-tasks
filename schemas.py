from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime


class TaskCreateSchema(BaseModel):
    title: constr(min_length=1)
    description: Optional[str]


class TaskUpdateSchema(BaseModel):
    title: Optional[constr(min_length=1)]
    description: Optional[str]


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
