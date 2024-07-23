from typing import List, Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import AccidentDAL, UserDAL
from db.session import get_db

from schemas.accidents import AccidentCreate, AccidentUpdate, Accident, ShowBuilding
from schemas.users import User

from services.building import Building
from services.auth import authenticate, create_access_token


router = APIRouter()


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


@router.post("/", response_model=Accident)
async def create_accident(body: AccidentCreate, db: AsyncSession = Depends(get_db)) -> Accident:
    return await _create_accident(body, db)


@router.patch("/{uuid}", response_model=Accident)
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


@router.get("/{uuid}", response_model=Accident)
async def get_accident_by_uuid(uuid: UUID, db: AsyncSession = Depends(get_db)) -> Accident:
    accident = await _get_accident(uuid, db)
    if accident is None:
        raise HTTPException(status_code=404, detail=f"Accident with uuid {uuid} not found")
    return accident


@router.get("/", response_model=List[Accident])
async def get_accidents(db: AsyncSession = Depends(get_db)) -> List[Accident]:
    accidents = await _get_accidents(db)
    if accidents is None:
        return []
    return accidents


"""USER TEST"""

async def _get_user_by_username(username: str, db):
    async with db as session:
        async with session.begin():
            print('handlers')
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_username(username=username, db=db)
            print(user)
            if user is not None:
                return User.model_validate(user, from_attributes=True)


@router.get('/user/', response_model=User)
async def get_user_by_username1(username: str, db: AsyncSession = Depends(get_db)) -> User:
    user = await _get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found.")
    return user


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    print("login!")
    user = await authenticate(username=form_data.username, password=form_data.password, db=db)
    print(user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "acces_token": "test", # create_access_token(sub=user.id),
        "token_type": "bearer",
    }




"""depr: """


@router.get("/accident_area")
async def accident_area(object_id: str) -> ShowBuilding:
    print('start')
    building = await _get_accident_area(object_id)
    if not building:
        raise HTTPException(status_code=404, detail=f"Object with id {object_id} not found.")

    return building



