from sqlalchemy import event

from db.session import engine
from .models import Accident


@event.listens_for(Accident, 'after_insert', asyncio=True)
async def after_insert_subject_status(mapper, connection, target):
    print("eveeeeeeenttttt yeah!!")


@event.listens_for(engine.sync_engine, "connect")
def my_on_connect(dbapi_con, connection_record):
    print("New DBAPI connection:", dbapi_con)
