from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.api import api_router
import settings


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
