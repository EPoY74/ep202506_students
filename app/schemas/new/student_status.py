"""
Pydantic схема для модели StudentStatus
"""

from pydantic import BaseModel


class StudentStatusBase(BaseModel):
    status_code: str
    status_label: str


class StudentStatusCreate(StudentStatusBase):
    pass


class StudentStatusRead(StudentStatusBase):
    status_id: int

    class Config:
        from_attributes = True
