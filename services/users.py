from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.users import User


async def create_user(session: AsyncSession, name: str, email: str) -> User:
    user = User(name=name, email=email)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
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
