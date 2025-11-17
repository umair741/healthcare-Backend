from sqlalchemy import Column, String, TIMESTAMP,Boolean
from sqlalchemy.orm import relationship
from db import Base
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

   
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,index= True)
    national_id = Column(String(20), unique=True, nullable=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, server_default="true")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    doctor = relationship("Doctor", back_populates="user", uselist=False)
