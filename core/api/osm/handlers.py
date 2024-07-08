from fastapi import APIRouter

from services.osm_services import entry_point, get_accident_area


osm_router = APIRouter(tags=['OSM'])


@osm_router.get("/nearest")
async def get_nearest(lat, lon):
    return entry_point(lat, lon)


@osm_router.get("/accident_area")
async def accident_area(object_id):
    return get_accident_area(object_id)
