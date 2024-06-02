from fastapi import APIRouter

from .services import entry_point


osm_router = APIRouter(tags=['OSM'])


@osm_router.get("/nearest")
async def get_nearest(lat, lon):
    return entry_point(lat, lon)
