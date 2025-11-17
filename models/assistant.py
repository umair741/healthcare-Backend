from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from db import Base
import uuid

class Assistant(Base):
    __tablename__ = "assistant"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.user_id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    doctor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("doctor.user_id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    appointed_on = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
