import uuid
from typing import Optional, List

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class AccidentCreate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    building_id: str
    note: str
    #created_by: int


class AccidentUpdate(BaseModel):
    note: Optional[str]
    is_active: Optional[bool]


class AccidentNodes(BaseModel):
    node: Optional[List[float]]


class Accident(TunedModel):
    uuid: uuid.UUID
    latitude: Optional[float]
    longitude: Optional[float]
    building_id: str
    note: str
    user_id: int
    nodes: Optional[List[List[float]]]


class AccidentList(TunedModel):
    accidents: List[Accident]


class ShowBuilding(BaseModel):
    building_id: str
    nodes: list
    nodes_convex_hull: list
    accident_area: list
