from fastapi import FastAPI, APIRouter

from api.bts.handlers import bts_router
from api.osm.handlers import osm_router

app = FastAPI(title="savr-parking")

main_api_router = APIRouter()

main_api_router.include_router(bts_router)
main_api_router.include_router(osm_router)
app.include_router(main_api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
