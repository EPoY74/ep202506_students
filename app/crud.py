from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Student
from app.schemas import UserCreate


async def get_users(db: AsyncSession):
    result = await db.execute(select(Student))
    return result.scalars().all()


async def get_user(db: AsyncSession, user_id: int):
    return await db.get(Student, user_id)


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = Student(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    user = await db.get(Student, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
