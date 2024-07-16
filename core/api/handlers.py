from typing import Union, List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from pydantic import parse_obj_as, TypeAdapter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import AccidentDAL
from db.session import get_db
from settings import BTS_TOKEN, TRACKED_VEHICLES
from .models import ShowBuilding, AccidentCreate, AccidentUpdate, Accident

from services.bts_services import BtsAPIClient
from services.osm_services import entry_point, get_accident_area
from services.building import Building


parking_router = APIRouter(tags=['parking'])

bts_client = BtsAPIClient(token=BTS_TOKEN)


async def _get_accident_area(object_id):
    if not object_id:
        return None

    building = Building(object_id=object_id, distance=50)
    print(building)
    return ShowBuilding(
        building_id=building.object_id,
        nodes=building.nodes,
        nodes_convex_hull=building.nodes_convex_hull,
        accident_area=building.accident_area
    )


"""TEST"""
async def _create_accident(body: AccidentCreate, db) -> Accident:
    async with db as session:
        async with session.begin():
            accident_dal = AccidentDAL(session)
            accident = await accident_dal.create_accident(
                building_id=body.building_id,
                note=body.note
            )
            return Accident(
                uuid=accident.uuid,
                latitude=accident.latitude,
                longitude=accident.longitude,
                building_id=accident.building_id,
                note=accident.note
            )


async def _update_accident(uuid: UUID, updated_fields: dict, db) -> Accident:
    async with db as session:
        async with session.begin():
            accident_dal = AccidentDAL(session)
            updated_user_id = await accident_dal.update_accident(uuid=uuid, **updated_fields)
            return updated_user_id


async def _get_accident(uuid, db):
    async with db as session:
        async with session.begin():
            accident_dal = AccidentDAL(session)
            accident = await accident_dal.get_accident_by_uuid(uuid=uuid)
            if accident is not None:
                return Accident.model_validate(accident, from_attributes=True)


async def _get_accidents(db):
    async with db as session:
        async with session.begin():
            accident_dal = AccidentDAL(session)
            accidents = await accident_dal.get_accidents()
            if accidents is not None:
                result = [Accident.model_validate(accident, from_attributes=True) for accident in accidents]
                return result


@parking_router.post("/", response_model=Accident)
async def create_accident(body: AccidentCreate, db: AsyncSession = Depends(get_db)) -> Accident:
    return await _create_accident(body, db)


@parking_router.post("/{uuid}", response_model=Accident)
async def update_accident(uuid: UUID, body: AccidentUpdate, db: AsyncSession = Depends(get_db)) -> Accident:
    #updated_fields = body.dict(exclude_none=True)
    updated_fields = body.dict()
    if updated_fields == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided"
        )
    accident_for_update = await _get_accident(uuid, db)
    if accident_for_update is None:
        raise HTTPException(
            status_code=404,
            detail=f"Accident with id {uuid} not found."
        )

    try:
        updated_accident = await _update_accident(updated_fields=updated_fields, db=db, uuid=uuid)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail="Something went wrong")

    return  "yeah"


@parking_router.get("/{uuid}", response_model=Accident)
async def get_accident_by_uuid(uuid: UUID, db: AsyncSession = Depends(get_db)) -> Accident:
    accident = await _get_accident(uuid, db)
    if accident is None:
        raise HTTPException(status_code=404, detail=f"Accident with uuid {uuid} not found")
    return accident


@parking_router.get("/", response_model=List[Accident])
async def get_accidents(db: AsyncSession = Depends(get_db)) -> List[Accident]:
    accidents = await _get_accidents(db)
    if accidents is None:
        return []
    return accidents



@parking_router.get("/accident_area")
async def accident_area(object_id: str) -> ShowBuilding:
    print('start')
    building = await _get_accident_area(object_id)
    if not building:
        raise HTTPException(status_code=404, detail=f"Object with id {object_id} not found.")

    return building


@parking_router.get("/vehicles")
async def get_vehicles():
    vehicles = bts_client.get_vehicle_list()
    vehicles_filtered = list(filter(lambda item: item['object_id'] in TRACKED_VEHICLES, vehicles))
    return vehicles_filtered


@parking_router.get("/current_position")
async def get_current_position(object_id: str | None = None,):
    response = bts_client.get_current_position(object_id)
    response_filtered = list(filter(lambda vehicle: vehicle['object_id'] in TRACKED_VEHICLES, response))
    response_filtered = response_filtered + list(filter(lambda vehicle: 'android_state' in vehicle, response))
    for item in response_filtered:
        item['parking'] = True
    return response_filtered






