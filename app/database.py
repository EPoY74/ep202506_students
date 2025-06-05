"""
Работа с БД
Иициализация БД
"""

import logging
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

import dotenv


class EnverontmentVariableNotFound(BaseException):
    """
    Класс для пробрасвания своих ошибок
    """

    pass


class Base(DeclarativeBase):
    pass


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


if not os.getenv("DB_USER") or len(str(os.getenv("DB_USER"))) < 2:
    err_message = (
        "Переменная DB_USER ( Имя пользователя БД) в памяти не найдена."
    )
    logging.warning(err_message)
if not os.getenv("DB_PASSWORD") or len(str(os.getenv("DB_PASSWORD"))) < 2:
    err_message = (
        "Переменная DB_PASSWORD (Пароль пользователя БД) в памяти  не найдена."
    )
    logging.warning(err_message)
if not os.getenv("DB_HOST") or len(str(os.getenv("DB_HOST"))) < 2:
    err_message = "Переменная DB_HOST (Хост БД) в памяти  не найдена."
    logging.warning(err_message)
if not os.getenv("DB_PORT") or len(str(os.getenv("DB_PORT"))) < 2:
    err_message = (
        "Переменная DB_PORT (Порт подключения к БД) в памяти  не найдена."
    )
    logging.warning(err_message)
if not os.getenv("DB_NAME") or len(str(os.getenv("DB_NAME"))) < 2:
    err_message = "Переменная DB_NAME (Имя БД) в памяти  не найдена."
    logging.warning(err_message)

if not dotenv.load_dotenv():
    err_message = "Файл .env с настройками не найден"
    logging.error(err_message)
    raise (EnverontmentVariableNotFound(err_message))
else:
    info_message = "Найден и загружен файл с настройками .env"
    logging.info(info_message)

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
