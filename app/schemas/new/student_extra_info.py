"""
Pydantic схема для модели StudentExtraInfo
"""

from datetime import datetime
from pydantic import BaseModel


class StudentExtraInfoBase(BaseModel):
    info_type: str
    info_value: str


class StudentExtraInfoCreate(StudentExtraInfoBase):
    student_id: int


class StudentExtraInfoRead(StudentExtraInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
