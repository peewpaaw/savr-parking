import uuid
from enum import Enum

from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, BIGINT, func
from sqlalchemy.dialects.postgresql import UUID, ENUM, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy import event


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


class SubjectType(Enum):
    vehicle = "VEHICLE"
    mobile = "MOBILE"


class Subject(Base):
    __tablename__ = "subject"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(ENUM(SubjectType), nullable=False)
    bts_id = Column(Integer, nullable=True)
    statuses = relationship("SubjectStatus", back_populates="subject")


class SubjectStatus(Base):
    __tablename__ = "subject_status"
    id = Column(Integer, primary_key=True)
    subject_uuid = Column(UUID, ForeignKey("subject.uuid"))
    subject = relationship(Subject, back_populates='statuses')
    datetime_entry = Column(TIMESTAMP, server_default=func.now())
    datetime_unix = Column(BIGINT, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)



