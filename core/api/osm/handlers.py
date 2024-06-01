from fastapi import APIRouter

from services.osm import get_nearest_buildings, get_rectangle_points, get_way_nodes, entry_point
from .models import BuildingList, Building


osm_router = APIRouter(tags=['OSM'])


@osm_router.get("/nearest")
async def get_nearest(lat, lon):
    return entry_point(lat, lon)
    # buildins_id = get_nearest_buildings(lat, lon)
    # test = [get_way_nodes(building_id) for building_id in buildins_id]
    # return BuildingList(test)
    #return response


@osm_router.get("/rectangle-nodes")
async def get_rectangle_nodes(lat, lon):
    buildings_nodes = get_nearest_buildings(lat, lon)
    ractangles = [get_rectangle_points(node) for node in buildings_nodes]
    return ractangles

@osm_router.get("/test")
async def test() -> Building:
    test_data = {'id': '1', 'nodes': []}
    print(test_data['id'])
    return Building(id=test_data['id'], nodes=test_data['nodes'])

