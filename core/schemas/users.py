from typing import Optional, Union

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    ...


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


