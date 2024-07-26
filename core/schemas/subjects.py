import uuid
from typing import Optional, List

from pydantic import BaseModel
from db.models import SubjectType


class Subject(BaseModel):
    uuid: uuid.UUID
    type: str
    bts_id: Optional[int]


class SubjectCreate(BaseModel):
    type: SubjectType
    bts_id: Optional[int]



