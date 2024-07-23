from fastapi import APIRouter

from . import accidents, users, bts


api_router = APIRouter()
api_router.include_router(accidents.router, prefix="/accidents", tags=["accidents"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(bts.router, prefix="/bts", tags=["bts"])
