import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Student
from app.schemas.schemas import StudentCreate, StudentRead

logger = logging.getLogger(__name__)


async def get_users(db: AsyncSession):
    result = await db.execute(select(Student))
    return result.scalars().all()


async def get_user(db: AsyncSession, user_id: int):
    result = await db.get(Student, user_id)
    return result


async def create_user(db: AsyncSession, user: StudentCreate):
    db_user = Student(**user.model_dump())
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as err:
        err_str = str(err)
        if "unique constraint" in err_str and "ix_students_email" in err_str:
            logger.error(str(err))
            raise HTTPException(
                status_code=409,
                detail={"message": "Email already exists", "field": "email"}
            )
    


async def delete_user(db: AsyncSession, user_id: int):
    user = await db.get(Student, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False


async def delete_user_check(db: AsyncSession, user_id: int):
    user = await db.get(Student, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return StudentRead.model_validate(user)
    return None

