from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.users import get_current_user
from db.dals import SubjectDAL
from db.models import Subject
from db.session import get_db

from schemas.subjects import Subject, SubjectCreate


router = APIRouter(
    #dependencies=[Depends(get_current_user)]
)


async def _get_subjects(db: AsyncSession):
    async with db as session:
        async with session.begin():
            subject_dal = SubjectDAL(session)
            subjects = await subject_dal.get_subjects()
            if subjects is not None:
                result = [Subject.model_validate(subject, from_attributes=True) for subject in subjects]
                return result


async def _create_subject(body: SubjectCreate, db: AsyncSession):
    async with db as session:
        async with session.begin():
            subject_dal = SubjectDAL(session)
            subject = await subject_dal.create_subject(
                type=body.type,
                bts_id=body.bts_id
            )
            return Subject.model_validate(subject, from_attributes=True)


@router.get("/", response_model=List[Subject])
async def get_accidents(
        db: AsyncSession = Depends(get_db)
) -> List[Subject]:
    subjects = await _get_subjects(db)
    if subjects is None:
        return []
    return subjects


@router.post("/", response_model=Subject)
async def get_accidents(
        body: SubjectCreate,
        db: AsyncSession = Depends(get_db)
) -> List[Subject]:
    return await _create_subject(body=body, db=db)
