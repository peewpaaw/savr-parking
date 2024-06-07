from fastapi import APIRouter

from settings import BTS_TOKEN
from services.bts_services import BtsAPIClient


SAVR_VEHICLES = ["5746200", "5746207", "1985488", "2651742", "5383695", "1985696", "1986136", "5733383",
                 "5733374", "5427501", "5383755", "5536815", "5536816", "1985485", "5383756", "5734617"]

bts_router = APIRouter(tags=['BTS'])

bts_client = BtsAPIClient(token=BTS_TOKEN)


@bts_router.get("/vehicles")
async def get_vehicles():
    vehicles = bts_client.get_vehicle_list()
    vehicles_filtered = list(filter(lambda item: item['object_id'] in SAVR_VEHICLES, vehicles))
    return vehicles_filtered


@bts_router.get("/current_position")
async def get_current_position(object_id: str | None = None):
    response = bts_client.get_current_position(object_id)
    response_filtered = list(filter(lambda item: item['object_id'] in SAVR_VEHICLES, response))
    return response_filtered
