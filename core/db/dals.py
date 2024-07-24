from uuid import UUID

from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Accident, User


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
        self.db_session.add(new_accident)
        await self.db_session.flush()
        return new_accident

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
