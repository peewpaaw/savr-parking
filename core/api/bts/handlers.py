from fastapi import APIRouter

from settings import BTS_TOKEN, TRACKED_VEHICLES
from services.bts_services import BtsAPIClient

from services.osm_services import entry_point


# SAVR_VEHICLES = ["5746200", "5746207", "1985488", "2651742", "5383695", "1985696", "1986136", "5733383",
#                  "5733374", "5427501", "5383755", "5536815", "5536816", "1985485", "5383756", "5734617"]

bts_router = APIRouter(tags=['BTS'])

bts_client = BtsAPIClient(token=BTS_TOKEN)


@bts_router.get("/vehicles")
async def get_vehicles():
    vehicles = bts_client.get_vehicle_list()
    vehicles_filtered = list(filter(lambda item: item['object_id'] in TRACKED_VEHICLES, vehicles))
    return vehicles_filtered


@bts_router.get("/current_position")
async def get_current_position(object_id: str | None = None):
    response = bts_client.get_current_position(object_id)
    response_filtered = list(filter(lambda vehicle: vehicle['object_id'] in TRACKED_VEHICLES, response))
    response_filtered = response_filtered + list(filter(lambda vehicle: 'android_state' in vehicle, response))
    for item in response_filtered:
        item['parking'] = True
        if 'latitude' in item and item['speed'] == "0" and 'android_state' not in item:
            nearest_buildings = entry_point(item['latitude'], item['longitude'])
            if len(nearest_buildings) > 0:
                parking = [building['parking'] for building in nearest_buildings]
                item['parking'] = False if False in parking else True
    return response_filtered
