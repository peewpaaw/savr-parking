from fastapi import APIRouter

from settings import BTS_TOKEN
from .services import BtsAPIClient

bts_router = APIRouter(tags=['BTS'])

bts_client = BtsAPIClient(token=BTS_TOKEN)


@bts_router.get("/vehicles")
async def get_vehicles():
    vehicles = bts_client.get_vehicle_list()
    return vehicles


@bts_router.get("/current_position")
async def get_current_position(object_id: str | None):
    response = bts_client.get_current_position(object_id)
    return response
