from pydantic import BaseModel, Field


class UserGetSchema(BaseModel):
    user_id: int

class UserCreateSchema(BaseModel):
    login: str = Field(max_length=50)
    password: str = Field(max_length=64)

class UserUpdateSchema(BaseModel):
    login: str | None = Field(max_length=50, default=None)
    password: str | None = Field(max_length=64, default=None)

class UserDeleteSchema(BaseModel):
    user_id: int
