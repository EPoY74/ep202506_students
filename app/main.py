"""
https://github.com/EPoY74/ep202506_students
API для работы со студентами
"""

import logging
import sys

from typing import Any, AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session, engine, Base
from contextlib import asynccontextmanager
from app import crud
from app.schemas import schemas
from app.models import StudentStatus


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log", encoding="utf-8"),
        ],
    )


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Создает таблицы при первом запуске
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield

    async with AsyncSession(engine) as session:
        result = await session.execute(select(func.count()).select_from(StudentStatus))
        student_status_count = result.scalar()
        logging.info("")

        if student_status_count == 0:
            student_status = [
                # StudentStatus(name="Alice", email="alice@example.com"),
                # StudentStatus(name="Bob", email="bob@example.com")
                StudentStatus(status_code="active", status_label="Обучается"),
                StudentStatus(
                    status_code="academic_leave", status_label="Академический отпуск"
                ),
                StudentStatus(status_code="expelled", status_label="Отчислен"),
                StudentStatus(status_code="reinstated", status_label="Восстановлен"),
                StudentStatus(
                    status_code="graduated", status_label="Завершил обучение"
                ),
                StudentStatus(status_code="transferred", status_label="Переведён"),
                StudentStatus(
                    status_code="postgraduate", status_label="Продолжает обучение"
                ),
                StudentStatus(
                    status_code="debt", status_label="Академическая задолженность"
                ),
            ]
            await session.add_all(student_status)
            await session.commit()


app = FastAPI(lifespan=lifespan)


# Зависимость
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Создает сессию для работы с БД
    """
    async with async_session() as session:
        yield session


@app.post("/users/", response_model=schemas.StudentRead)
async def create_user(user: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    """
    Создает пользователя
    """
    return await crud.create_user(db, user)


@app.get("/users/", response_model=list[schemas.StudentRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    """
    Читает все пользователей
    """
    return await crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.StudentRead)
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
