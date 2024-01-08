from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.db.tables import users as users_db


router = APIRouter()


@router.get("/user")
async def user_get(user_id: int,
                   session: AsyncSession = Depends(get_db)):
    user = await users_db.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(400, detail="User not found")

    return user

