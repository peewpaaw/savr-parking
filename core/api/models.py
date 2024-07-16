import re
import uuid
from typing import Optional, List

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class AccidentCreate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    building_id: str
    note: str


class AccidentUpdate(BaseModel):
    note: Optional[str]
    is_active: Optional[bool]


class Accident(TunedModel):
    uuid: uuid.UUID
    latitude: Optional[float]
    longitude: Optional[float]
    building_id: str
    note: str


class AccidentList(TunedModel):
    accidents: List[Accident]



class ShowBuilding(BaseModel):
    building_id: str
    nodes: list
    nodes_convex_hull: list
    accident_area: list





