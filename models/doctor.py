from sqlalchemy import Column, String,TIMESTAMP,ForeignKey,Integer,Enum
from db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

class VerificationEnum(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class doctor(Base):
    __tablename__ = "doctor"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),primary_key=True,index= True )
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinic.id", ondelete="CASCADE"),index= True )
    specialization = Column(String)
    qualifications = Column(String)
    license_number = Column(String,unique=True)
    about = Column(String(500))
    experience_years = Column(Integer)
    verification_status = Column(Enum(VerificationEnum),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),server_default=func.now())


