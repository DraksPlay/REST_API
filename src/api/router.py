from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib

from db.session import get_db
from db.tables import users as users_db
from api.schemas import (
    UserGetSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserDeleteSchema
)


router = APIRouter()


@router.get("/user")
async def user_get(user_schema: UserGetSchema = Depends(),
                   session: AsyncSession = Depends(get_db)):
    user = await users_db.get_user_by_id(session, user_schema.user_id)
    if user is None:
        raise HTTPException(400, detail="User not found")

    return user

@router.post("/user")
async def user_create(user_schema: UserCreateSchema,
                      session: AsyncSession = Depends(get_db)):
    hash_password = hashlib.sha256(user_schema.password.encode("utf-8")).hexdigest()
    user = await users_db.create_user(session, user_schema.login, hash_password)

    return user

@router.patch("/user")
async def user_update(user_id: int,
                      user_schema: UserUpdateSchema,
                      session: AsyncSession = Depends(get_db)):
    if user_schema.password is not None:
        user_schema.password = hashlib.sha256(user_schema.password.encode("utf-8")).hexdigest()
    update_params = dict(filter(lambda x: x[1] is not None, user_schema))
    user = await users_db.update_user(session,
                                      user_id=user_id,
                                      **dict(update_params)
                                      )
    return user

@router.delete("/user")
async def user_delete(user_schema: UserDeleteSchema = Depends(),
                      session: AsyncSession = Depends(get_db)):
    user = await users_db.delete_user(session, user_schema.user_id)

    return user
