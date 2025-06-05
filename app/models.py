from sqlalchemy import String, Integer  
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    """
    Класс модели пользователя для таблицы users в БД

    Атрибуты:

    __tablename__(str): Наименование таблицы в БД
    id (int) - Уникальный ИД пользователя (первичный ключ)
    name (str) - Имя пользователя
    email (str) - Электронная почта пользователя (Уникальный)
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
