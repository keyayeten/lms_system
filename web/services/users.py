from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from web.models.users import User

from web.core.security import get_password_hash


async def create_user(session: AsyncSession, user: User) -> User:
    hashed_password = get_password_hash(user.password)
    user = User(
        username=user.name,
        hashed_password=hashed_password,
        email=user.email
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, name: str) -> User | None:
    result = await session.execute(select(User).where(User.name == name))
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await get_user(session, user_id)
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False
