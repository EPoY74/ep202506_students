"""
Pydantic-схемы для работы с пользователями (создание, чтение и т.д.)
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Базовая схема пользователя 
    """
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Схема для создания нового пользователя.
    """
    pass


class UserRead(UserBase):
    """
    Схема для чтения информации о пользователе
    """
    id: int

    class Config:
        from_attributes = True  # Важно для совместимости с ORM
