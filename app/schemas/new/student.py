"""
Pydantic схема для модели Student
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr
from app.schemas.student_status import StudentStatusRead
from app.schemas.student_extra_info import StudentExtraInfoRead


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    status_code: str


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentReadFull(StudentRead):
    status: StudentStatusRead
    extra_info: List[StudentExtraInfoRead] = []

    class Config:
        from_attributes = True
