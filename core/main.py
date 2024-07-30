from typing import Annotated

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from db import event_listeners

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
    pass
    #scheduler.start()
    #scheduler.add_job(scheduler_task, IntervalTrigger(minutes=1))


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello")
async def hello(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}



"""
    websocket
"""

# class ConnectionManager:
#     """Class defining socket events"""
#
#     def __init__(self):
#         """init method, keeping track of connections"""
#         self.active_connections = []
#
#     async def connect(self, websocket: WebSocket):
#         """connect event"""
#         await websocket.accept()
#         self.active_connections.append(websocket)
#
#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         """Direct Message"""
#         await websocket.send_text(message)
#
#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)
#
#     def disconnect(self, websocket: WebSocket):
#         """disconnect event"""
#         self.active_connections.remove(websocket)


# manager = ConnectionManager()
#
#
# @app.websocket("/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")
#
#
# @app.websocket("/")
# async def websocket_test(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"{data} suck my dick", websocket)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.send_personal_message("bye!", websocket)
