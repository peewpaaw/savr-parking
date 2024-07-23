from datetime import timedelta
from typing import Any, Annotated

import jwt
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from db.dals import UserDAL
from db.session import get_db
from schemas.users import User, TokenData
from services.auth import oauth2_scheme, authenticate, create_access_token


router = APIRouter()


async def _get_user_by_username(username: str, db):
    async with db as session:
        async with session.begin():
            print('handlers')
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_username(username=username)
            print(user)
            if user is not None:
                return User.model_validate(user, from_attributes=True)


@router.get('/get-user-by-username', response_model=User)
async def get_user_by_username1(username: str, db: AsyncSession = Depends(get_db)) -> User:
    user = await _get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found.")
    return user


@router.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    user = await authenticate(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print("current_user payload", payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await _get_user_by_username(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


@router.get('/me', response_model=User)
async def users_me(current_user: User = Depends(get_current_user)):
    return current_user
