"""
https://github.com/EPoY74/ep202506_students
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session, engine, Base
import crud
import schemas

app = FastAPI()

# Создание таблиц
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Зависимость
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.post("/users/", response_model=schemas.UserRead)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_users(db)

@app.get("/users/{user_id}", response_model=schemas.UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
