from sqlalchemy import Column, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from db import Base


class UserRole(Base):
    __tablename__ = "user_role"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    role_id = Column(
        Integer,
        ForeignKey("role.id", ondelete="CASCADE"),
        primary_key=True,
    )

    assigned_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
