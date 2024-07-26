from typing import Annotated

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from apscheduler.schedulers.background import BackgroundScheduler
from tasks import scheduler_task

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

# scheduler = BackgroundScheduler()
# scheduler.add_job(test_task, 'interval', seconds=10)
# scheduler.start()

scheduler = AsyncIOScheduler()
#scheduler.add_job(async_task, 'interval', seconds=3)
#scheduler.start()


@app.on_event("startup")
async def startup_event():
    #pass
    scheduler.start()
    scheduler.add_job(scheduler_task, IntervalTrigger(minutes=10))


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello")
async def hello(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
