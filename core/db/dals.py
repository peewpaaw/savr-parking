from uuid import UUID

from sqlalchemy import update, and_, select, desc, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Engine

from .models import Accident, User, Subject, SubjectStatus
from services.building import Building

import settings


class AccidentDAL:
    """Data Access Layer for accident"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_accident(
            self,
            building_id: str,
            user_id: int,
            latitude: float | None = None,
            longitude: float | None = None,
            note: str | None = None,

    ) -> Accident:
        new_accident = Accident(
            building_id=building_id,
            note=note,
            latitude=latitude,
            longitude=longitude,
            user_id=user_id
        )
        new_accident.nodes = self._get_accident_area(new_accident.building_id)
        self.db_session.add(new_accident)
        await self.db_session.flush()
        return new_accident

    def _get_accident_area(self, building_id: str):
        building = Building(
            object_id=building_id,
            distance=settings.ACCIDENT_DISTANCE
        )
        return building.accident_area

    async def update_accident(
            self, uuid: UUID, **kwargs
    ):
        query = (
            update(Accident)
            .where(Accident.uuid == uuid)
            .values(kwargs)
            .returning(Accident.uuid)
        )
        res = await self.db_session.execute(query)
        update_accident_id_row = res.fetchone()
        if update_accident_id_row is not None:
            return update_accident_id_row[0]

    async def get_accident_by_uuid(self, uuid: UUID):
        query = select(Accident).where(Accident.uuid == uuid)
        res = await self.db_session.execute(query)
        accident = res.fetchone()
        if accident is not None:
            return accident[0]

    async def get_accidents(self):
        query = select(Accident)
        res = await self.db_session.execute(query)
        # accidents = res.all()#res.fetchall()
        accidents = res.scalars().all()
        if accidents is not None:
            return accidents


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_username(self, username: str):
        query = select(User).where(User.username == username)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]


class SubjectDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_subject(
            self,
            type: str,
            bts_id: int | None = None

    ) -> Subject:
        new_subject = Subject(
            type=type,
            bts_id=bts_id
        )
        self.db_session.add(new_subject)
        await self.db_session.flush()
        return new_subject

    async def add_subject_status(
            self,
            subject_uuid: UUID,
            datetime_unix,
            latitude: float,
            longitude: float,
            speed: float,
    ):
        # subject_q = await self.db_session.execute(select(Subject).where(bts_id=bts_id))
        # subject = subject_q.fetchone()
        # if subject is not None:
        subject_status = SubjectStatus(
            subject_uuid=subject_uuid,
            datetime_unix=datetime_unix,
            latitude=latitude,
            longitude=longitude,
            speed=speed
        )
        self.db_session.add(subject_status)
        await self.db_session.flush()
        return subject_status

    async def get_subjects(self, uuid: UUID | None = None):
        query = select(Subject)
        if uuid:
            query = query.where(uuid=uuid)
        res = await self.db_session.execute(query)
        subjects = res.scalars().all()
        if subjects:
            return subjects

    async def get_bts_subject(self):
        query = select(Subject).where(Subject.bts_id is not None)
        result = await self.db_session.execute(query)
        subjects = result.scalars().all()
        if subjects:
            return subjects

    async def get_subject_status(self, uuid):
        query = select(SubjectStatus)\
            .join(Subject)\
            .filter(Subject.uuid == uuid)\
            .order_by(desc(SubjectStatus.datetime_entry))
        result = await self.db_session.execute(query)
        subject_status = result.fetchone()
        if subject_status:
            return subject_status



        # .join(Subject) \
        #     .filter(Subject.uuid == subject_uuid) \
        #     .order_by(desc(SubjectStatus.datetime_entry)) \
        #     .first()



# before_execute event on all Engine instances
@event.listens_for(Engine, "before_execute")
def my_before_execute(
    conn,
    clauseelement,
    multiparams,
    params,
    execution_options,
):
    print("before execute!")


