from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from db import Base
import uuid
import enum


class StatusEnum(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class DoctorVerification(Base):
    __tablename__ = "doctor_verification"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,               # fixed: Index -> index
    )

    doctor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("doctor.user_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    DegreePath = Column(String(length=250), nullable=False)
    nationalCardFront = Column(String(length=250), nullable=False)
    nationalCardBack = Column(String(length=250), nullable=False)
    doctorCard = Column(String(length=250), nullable=False)

    status = Column(
        Enum(StatusEnum),
        nullable=False,
        default=StatusEnum.pending,   # Python-side default
        # you can also add server_default if you want DB-level default
        # server_default="pending"
    )
