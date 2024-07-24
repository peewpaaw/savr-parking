import uuid

from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()


class Accident(Base):
    __tablename__ = "accident"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    building_id = Column(String, nullable=True)
    note = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="accidents")
    nodes = Column(ARRAY(Float), nullable=True)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    accidents = relationship("Accident", back_populates="user")




