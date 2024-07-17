from fastapi import APIRouter

from services.bts_services import BtsAPIClient
from settings import TRACKED_VEHICLES, BTS_TOKEN


bts_router = APIRouter(tags=['bts'])

bts_client = BtsAPIClient(token=BTS_TOKEN)


@bts_router.get("/vehicles")
async def get_vehicles():
    vehicles = bts_client.get_vehicle_list()
    vehicles_filtered = list(filter(lambda item: item['object_id'] in TRACKED_VEHICLES, vehicles))
    return vehicles_filtered


@bts_router.get("/current_position")
async def get_current_position(object_id: str | None = None,):
    response = bts_client.get_current_position(object_id)
    response_filtered = list(filter(lambda vehicle: vehicle['object_id'] in TRACKED_VEHICLES, response))
    response_filtered = response_filtered + list(filter(lambda vehicle: 'android_state' in vehicle, response))
    for item in response_filtered:
        item['parking'] = True
    return response_filtered



