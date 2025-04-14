from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.core.db import get_session
from web.services.users_service import UserService


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService.create(session)
