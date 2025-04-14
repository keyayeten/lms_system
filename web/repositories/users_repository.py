from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web.models.users import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, name: str, email: str, hashed_password: str) -> User:
        user = User(name=name, email=email, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        user = await self.get_user(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False

    async def get_all_users(self) -> List[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()
