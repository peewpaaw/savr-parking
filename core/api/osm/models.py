from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr


class TunnedModel(BaseModel):
    pass


class Node(TunnedModel):
    lat: float
    lon: float


class Building(TunnedModel):
    id: str
    nodes: List[Node]


class BuildingList(TunnedModel):
    buildings: List[Building]
