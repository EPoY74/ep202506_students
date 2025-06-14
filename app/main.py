"""
https://github.com/EPoY74/ep202506_students
API для работы со студентами
"""

import logging
# import sys

from typing import Any, AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, event
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session, engine, Base
from contextlib import asynccontextmanager
from app import crud
from app.schemas import schemas
from app.models import StudentStatus


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        # handlers=[
        #     logging.StreamHandler(sys.stdout),
        #     logging.FileHandler("app.log", encoding="utf-8"),
        # ],
    )


setup_logging()
logger = logging.getLogger(__name__)

# Создаем обработчик события
def after_create(target, connection, **kw):
    logger.info("СТАРТ: Запуск инициализации таблицы StudentStatus начальными значениями")
    if not connection.execute(select(StudentStatus).limit(1)).fetchone():
        logger.info("НАЧАЛО: Инициализация таблицы StudentStatus")
        connection.execute(
            StudentStatus.__table__.insert(),
            [
                {"status_code": "active", "status_label": "Обучается"},
                {"status_code": "academic_leave", "status_label": "Академический отпуск"},
                {"status_code": "expelled", "status_label": "Отчислен"},
                {"status_code": "reinstated", "status_label": "Восстановлен"},
                {"status_code": "graduated", "status_label": "Завершил обучение"},
                {"status_code": "transferred", "status_label": "Переведён"},
                {"status_code": "postgraduate", "status_label": "Продолжает обучение"},
                {"status_code": "debt", "status_label": "Академическая задолженность"},
            ]
        )
        logger.info("КОНЕЦ: Инициализация таблицы StudentStatus")
        logger.info("ФИНИШ: Запуск инициализации таблицы StudentStatus начальными значениями")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Создает таблицы при первом запуске
    """
    async with engine.begin() as conn:
        logger.info('СТАРТ: Инициализация таблиц при первом запуске')
        # Подписываемся на событие
        event.listen(StudentStatus.__table__, 'after_create', after_create)
        await conn.run_sync(Base.metadata.create_all)
        logger.info('ФИНИШ: Инициализация таблиц при первом запуске')
        

    yield    

   
logger.info("Запуск приложения")
app = FastAPI(lifespan=lifespan)
logger.info("Приложение запущено")


# Зависимость
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Создает сессию для работы с БД
    """

    async with async_session() as session:
        logger.debug('Инициалзация сесии:')
        yield session


@app.post("/create_user/", response_model=schemas.StudentRead)
async def create_user(user: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    """
    Создает пользователя
    """
    logger.debug('Обращение post по /create_user/ создание пользователя')
    return await crud.create_user(db, user)


@app.get("/read_users/", response_model=list[schemas.StudentRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    """
    Читает все пользователей
    """
    logger.debug('Обращение get по /read_users/, все пользователи')
    return await crud.get_users(db)


@app.get("/read_user/{user_id}", response_model=schemas.StudentRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Читает одного пользователя
    """
    logger.debug('Чтение данных об одном пользователе по /read_user/')
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/user_delete/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удаляе одного пользователя
    """
    logger.debug('Обращение по /user_delete/ удаление пользователя')
    success = await crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
