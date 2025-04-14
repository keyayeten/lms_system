from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from web.models.users import User
from web.repositories.users_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @classmethod
    def create(cls, session: AsyncSession) -> 'UserService':
        repository = UserRepository(session)
        return cls(repository)

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repository.get_user(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.get_user_by_email(email)

    async def create_user(self, name: str, email: str, hashed_password: str) -> User:
        return await self.user_repository.create_user(name, email, hashed_password)

    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        return await self.user_repository.update_user(user_id, **kwargs)

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete_user(user_id)

    async def get_all_users(self) -> List[User]:
        return await self.user_repository.get_all_users()
