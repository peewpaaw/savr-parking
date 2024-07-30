from sqlalchemy.ext.asyncio import AsyncSession

import settings
from services.bts_services import BtsAPIClient
from db.dals import SubjectDAL
from db.session import get_db


bts_client = BtsAPIClient(settings.BTS_TOKEN)


async def scheduled_task(db_session: AsyncSession):
    async with db_session.begin():
        subject_dal = SubjectDAL(db_session)
        subjects_bts = await subject_dal.get_bts_subject()
        for subject in subjects_bts:
            subject_status_new = bts_client.get_current_position(object_id=subject.bts_id)
            if subject_status_new:
                subject_status_latest = await subject_dal.get_subject_status(uuid=subject.uuid)
                if not subject_status_latest or subject_status_latest[0].datetime_unix != subject_status_new[0]["datetime_unix"]:
                    await subject_dal.add_subject_status(
                        subject_uuid=subject.uuid,
                        datetime_unix=int(subject_status_new[0]["datetime_unix"]),
                        latitude=float(subject_status_new[0]["latitude"]),
                        longitude=float(subject_status_new[0]["longitude"]),
                        speed=float(subject_status_new[0]["speed"])
                    )




async def scheduler_task():
    """Wrapper to run the scheduled task within FastAPI dependency context"""
    async for db_session in get_db():
        await scheduled_task(db_session)
