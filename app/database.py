"""
Работа с БД
Иициализация БД
"""

import logging
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

import dotenv

logger = logging.getLogger(__name__)


class EnverontmentVariableNotFound(BaseException):
    """
    Класс для пробрасывания своих ошибок
    """

    pass


class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM-моделей проекта.
    Используется для регистрации всех моделей и доступа к общей metadata.
    """

    pass


if not os.getenv("DB_USER") or len(str(os.getenv("DB_USER"))) < 2:
    err_message = "Переменная DB_USER ( Имя пользователя БД) в памяти не найдена."
    logger.warning(err_message)
if not os.getenv("DB_PASSWORD") or len(str(os.getenv("DB_PASSWORD"))) < 2:
    err_message = (
        "Переменная DB_PASSWORD (Пароль пользователя БД) в памяти  не найдена."
    )
    logger.warning(err_message)
if not os.getenv("DB_HOST") or len(str(os.getenv("DB_HOST"))) < 2:
    err_message = "Переменная DB_HOST (Хост БД) в памяти  не найдена."
    logger.warning(err_message)
if not os.getenv("DB_PORT") or len(str(os.getenv("DB_PORT"))) < 2:
    err_message = "Переменная DB_PORT (Порт подключения к БД) в памяти  не найдена."
    logger.warning(err_message)
if not os.getenv("DB_NAME") or len(str(os.getenv("DB_NAME"))) < 2:
    err_message = "Переменная DB_NAME (Имя БД) в памяти  не найдена."
    logger.warning(err_message)


"""
# === Проверка переменных окружения ===
REQUIRED_ENV_VARS = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]

for var in REQUIRED_ENV_VARS:
    value = os.getenv(var)
    if not value or len(value.strip()) < 1:
        logger.warning(f"Переменная {var} не найдена или пуста")
"""

if not dotenv.load_dotenv():
    err_message = "Файл .env с настройками не найден"
    logger.error(err_message)
    raise (EnverontmentVariableNotFound(err_message))
else:
    info_message = "Найден и загружен файл с настройками .env"
    logger.info(info_message)

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
