from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.future import select

from web.core.db import get_session
from web.core.security import get_password_hash, verify_password, create_access_token
from web.models.users import User


auth = APIRouter(prefix="/auth")


@auth.post("/users/register")
async def register_user(request: Request):
    user_data = request.json()
    async for session in get_session():
        # Проверка на существующего пользователя по email
        stmt = select(User).where(User.email == user_data["email"])
        result = await session.execute(stmt)
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Хешируем пароль и создаём пользователя
        hashed_password = get_password_hash(user_data["password"])
        user = User(
            name=user_data["name"],
            email=user_data["email"],
            hashed_password=hashed_password
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }


@auth.post("/users/login")
async def login_user(request: Request):
    user_data = request.json()
    async for session in get_session():
        # Поиск по email
        stmt = select(User).where(User.email == user_data["email"])
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user or not verify_password(user_data["password"], user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Создание JWT-токена по email
        token = create_access_token({"sub": user.email})
        return {"access_token": token}
