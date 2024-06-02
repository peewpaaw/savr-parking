from typing import List

from pydantic import BaseModel


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
