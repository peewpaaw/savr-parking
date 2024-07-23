from datetime import datetime, timedelta, timezone
from typing import Annotated, Union, Optional

import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from passlib.context import CryptContext

from db.models import User
from db.dals import UserDAL
from settings import SECRET_KEY, ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate(username: str, password: str, db) -> Optional[User]:
    user_dal = UserDAL(db_session=db)
    user = await user_dal.get_user_by_username(username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return User



PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
