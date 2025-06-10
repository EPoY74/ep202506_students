import datetime

from sqlalchemy import String, Integer, ForeignKey, Index, DateTime, func, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class StudentStatus(Base):
    """
    Класс модели статус для связи с таблицей Students(Студенты)

    __tablename__="student_status" -название таблицы
    status_id (int) - Уникальный ID статуса (первичный ключ)
    status_code (str) - Код статуса сткдена (на английском)
    status_label (str) - Метка статуса студента (на русском)
    """

    __tablename__ = "student_status"
    status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    status_label: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    students: Mapped[list["Student"]] = relationship("Student", back_populates="status")


class StudentExtraInfo(Base):
    """
    Класс модели с дополнительной информацией о студенте

    __tablename__= 'student_extra_info' - Наименование  таблицы
    id (int) - Уникальный ID дополнительной информации
    student_id (int) - ID студента из таблицы students
    info_type (str) - Тип дополнительной информации (адрес, жалоба и др)
    info_value (str) - Дополнительная информация о студенте
    created_at (DateTime) - Дата создания дополнительной информации
    updated_at (DateTime) - Дата последноего изменения информации
    """

    __tablename__ = "student_extra_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"), nullable=False, index=True
    )
    info_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    info_value: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    student: Mapped["Student"] = relationship("Student", back_populates="extra_info")


class Student(Base):
    """
    Класс модели пользователя для таблицы students в БД

    Атрибуты:

    __tablename__(str): Наименование таблицы в БД
    id (int) - Уникальный ИД пользователя (первичный ключ)
    first_name (str) - Имя пользователя
    last_name (str) Фамилия пользователя
    email (str) - Электронная почта пользователя (Уникальный)
    created_at (DateTime) - Дата создания карточки студента
    updated_at (DateTime) - Дата последноего карточки студента
    """

    __tablename__ = "students"
    __table_args__ = (
        Index("ix_student_lastname_firstname", "last_name", "first_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), index=True)
    last_name: Mapped[str] = mapped_column(String(50))
    date_of_birth: Mapped[datetime.date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    status_code: Mapped[str] = mapped_column(ForeignKey("student_status.status_code"))

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    status: Mapped["StudentStatus"] = relationship(
        "StudentStatus", back_populates="students"
    )
    extra_info: Mapped[list["StudentExtraInfo"]] = relationship(
        "StudentExtraInfo", back_populates="student"
    )
