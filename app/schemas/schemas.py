"""
Pydantic-схемы для работы с пользователями (создание, чтение и т.д.)
"""

from pydantic import BaseModel, EmailStr
from datetime import date


class StudentBase(BaseModel):
    """
    Базовая схема пользователя 
    """
    first_name: str
    last_name: str
    email: EmailStr
    status_code: str
    date_of_birth: date



class StudentCreate(StudentBase):
    """
    Схема для создания нового пользователя.
    """
    pass


class StudentRead(StudentBase):
    """
    Схема для чтения информации о пользователе
    """
    id: int

    class Config:
        from_attributes = True  # Важно для совместимости с ORM
