from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.accidents import accidents_router
from api.bts import bts_router


app = FastAPI(title="savr-parking")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_api_router = APIRouter()
main_api_router.include_router(accidents_router, prefix="/accidents")
main_api_router.include_router(bts_router, prefix="/bts")

app.include_router(main_api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
