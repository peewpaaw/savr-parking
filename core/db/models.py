import uuid

from sqlalchemy import Column, String, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Accident(Base):
    __tablename__ = "accident"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    building_id = Column(String, nullable=True)
    note = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)


