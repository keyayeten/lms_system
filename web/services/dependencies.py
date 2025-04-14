from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.core.db import get_session
from web.services.users_service import UserService
from web.services.rabbit_service import RabbitService


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService.create(session)


async def get_rabbit_service() -> RabbitService:
    return RabbitService()
