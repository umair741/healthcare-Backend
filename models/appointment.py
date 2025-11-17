from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Enum
from db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

# ----------------- Appointment Status Enum -----------------
class AppointmentStatus(enum.Enum):
    PENDING = "pending"                         # Patient requested
    APPROVED = "approved"                       # Doctor accepted
    CANCELLED = "cancelled"                     # Doctor rejected
    IN_PROGRESS = "in_progress"                 # Appointment is happening
    COMPLETED = "completed"                     # Doctor finished
    RESCHEDULED = "rescheduled"

# ----------------- Appointment Table -----------------
class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    doctor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("doctor.user_id", ondelete="CASCADE"),
        index=True
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.user_id", ondelete="CASCADE"),
        index=True
    )

    clinic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("clinic.id", ondelete="CASCADE"),
        index=True
    )

    scheduled_start = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=True)
    scheduled_end = Column(TIMESTAMP(timezone=True))
    reason = Column(String)
    appointment_status = Column(Enum(AppointmentStatus), nullable=False)

   
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
