"""
https://github.com/EPoY74/ep202506_students
API для работы со студентами
"""

from typing import Any, AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session, engine, Base
from contextlib import asynccontextmanager
from app import crud
from app import schemas


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Создает таблицы при первом запуске
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield

app = FastAPI(lifespan=lifespan)

# Зависимость
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Создает сессию для работы с БД
    """
    async with async_session() as session:
        yield session


@app.post("/users/", response_model=schemas.UserRead)
async def create_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(get_db)
):
    """
    Создает пользователя
    """
    return await crud.create_user(db, user)


@app.get("/users/", response_model=list[schemas.UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    """
    Читает все пользователей
    """
    return await crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Читает одного пользователя
    """
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удаляе одного пользователя
    """
    success = await crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
