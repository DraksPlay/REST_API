from typing import Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


async def get_user_by_id(session: AsyncSession,
                         user_id: int,
                         ) -> Optional[User]:
    async with session.begin():
        query = select(User).where(User.id == user_id)
        res = await session.execute(query)
        user = res.scalar()
        return user

async def create_user(session: AsyncSession,
                      login: str,
                      password: str,
                      ) -> User:
    async with session.begin():
        user = User(
            login=login,
            password=password,
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user

async def update_user(session: AsyncSession,
                      user_id: int,
                      **kwargs
                      ) -> Optional[User]:
    async with session.begin():
        query = (
            update(User)
            .where(User.id == user_id)
            .values(kwargs)
            .returning(User)
        )
        res = await session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]

async def delete_user(session: AsyncSession,
                      user_id: int,
                      ) -> Optional[User]:
    async with session.begin():
        query = (
            delete(User)
            .where(User.id == user_id)
            .returning(User)
        )
        res = await session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]
