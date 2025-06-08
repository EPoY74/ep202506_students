from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    first_name: Mapped[str] = mapped_column("name", String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    status: Mapped[str] = mapped_column(ForeignKey("student_status.status_code"))

    student_status: Mapped["StudentStatus"] = relationship("StudentStatus", back_populates="users")


class StudentStatus(Base):
    """
    Класс можели ста1тус для связи с таблицей User(Студенты)

    __tablename__="student_status" -название таблицы
    status_id (int) - Уникальный ID статуса (первичный ключ)
    status_code (str) - Код статуса сткдена (на английском)
    status_label (str) - Метка статуса студента (на русском)
    """
    __tablename__="student_status"
    status_id: Mapped[int] = mapped_column(primary_key=True)
    status_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    status_label: Mapped[str] = mapped_column(String(30), nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="student_status") 