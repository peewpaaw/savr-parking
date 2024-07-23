from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from api.api import api_router
import settings
from services.auth import oauth2_scheme

app = FastAPI(title="savr-parking")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root_router = APIRouter()

app.include_router(root_router)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello")
async def hello(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
