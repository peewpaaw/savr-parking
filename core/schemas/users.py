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
