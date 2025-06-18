"""
https://github.com/EPoY74/ep202506_students
API для работы со студентами
"""

import logging
# import sys
from typing import Any, AsyncGenerator

from contextlib import asynccontextmanager, suppress
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy import select, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session, engine, Base

import uuid


from app import crud
from app.schemas import schemas
from app.models import StudentStatus


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
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


# Middleware для глобальной обработки ошибок
@app.middleware("http")
async def global_error_handler(request: Request, call_next):
    """
    Глобальный обработчик ошибок, который перехватывает все исключения,
    возникающие при обработке HTTP-запросов.
    
    Принцип работы:
    1. Пытается выполнить следующий middleware/обработчик запроса (call_next)
    2. Если возникает исключение - перехватывает его и возвращает соответствующий JSON-ответ
    3. Логирует все ошибки для последующего анализа
    """
    
    try:
        # Пробуем выполнить запрос
        return await call_next(request)
    
    except RequestValidationError as exc:
        """
        Обработка ошибок валидации входных данных (Pydantic).
        FastAPI автоматически генерирует эти ошибки при несоответствии данных схеме.
        """
        # Логируем информацию для отладки (уровень DEBUG чтобы не засорять логи в production)
        logger.debug("Validation error", exc_info=True)
        
        # Возвращаем ответ в формате, совместимом с Pydantic
        return JSONResponse(
            status_code=422,  # HTTP 422 Unprocessable Entity - стандартный код для ошибок валидации
            content={
                "detail": [
                    {
                        "type": error["type"],  # Тип ошибки (например, "value_error.missing")
                        "loc": error["loc"],  # Место возникновения ошибки (например, ["body", "username"])
                        "msg": error["msg"],  # Сообщение об ошибке
                        "input": error.get("input"),  # Неверные входные данные
                        "ctx": error.get("ctx")  # Дополнительный контекст
                    } for error in exc.errors()  # Преобразуем все ошибки в список
                ]
            }
        )
    
    except HTTPException as http_exc:
        """
        Обработка уже созданных HTTP-исключений.
        Эти исключения обычно создаются явно в коде обработчиков маршрутов.
        Мы просто передаем их дальше без изменений.
        """
        raise http_exc
    
    except SQLAlchemyError as db_exc:
        """
        Обработка ошибок базы данных (SQLAlchemy).
        Важно выполнить rollback транзакции и не раскрывать детали ошибки клиенту.
        """
        # Пытаемся выполнить rollback безопасно (suppress подавляет возможные исключения)
        with suppress(Exception):
            if hasattr(request.state, "db"):
                request.state.db.rollback()
        
        # Логируем полную ошибку для администратора
        logger.error("Database error", exc_info=True)
        
        # Возвращаем клиенту обобщенное сообщение
        return JSONResponse(
            status_code=400,  # HTTP 400 Bad Request - общий код для ошибок клиента
            content={
                "detail": [{
                    "type": "database_error",
                    "msg": "Database operation failed",
                    # В production показываем общее сообщение, в debug режиме - детали
                    "ctx": {"error": "Check logs for details"} if not app.debug else {"error": str(db_exc)}
                }]
            }
        )
    
    except Exception as exc:
        """
        Обработка всех неожиданных исключений (крайний случай).
        Генерируем уникальный ID ошибки для отслеживания и логируем полную информацию.
        """
        # Генерируем уникальный ID для ошибки
        error_id = uuid.uuid4()
        
        # Логируем критическую ошибку с полной информацией
        logger.critical(f"Unexpected error {error_id}: {exc}", exc_info=True)
        
        # Возвращаем клиенту сообщение с ID ошибки
        return JSONResponse(
            status_code=500,  # HTTP 500 Internal Server Error
            content={
                "detail": [{
                    "type": "server_error",
                    "msg": "Internal server error",
                    "error_id": str(error_id),  # Уникальный ID для поиска в логах
                    "info": "Contact support with this error_id"  # Инструкция для пользователя
                }]
            }
        )


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
