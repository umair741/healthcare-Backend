from sqlalchemy import Column, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class GenderEnum(enum.Enum):
    male = "Male"
    female = "Female"
   
class patients(Base):
    __tablename__ = "patients"
    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id", ondelete="CASCADE"),primary_key=True,index=True)
    dob = Column(Date)
    gender = Column(Enum(GenderEnum))
    phone = Column(String(20))
    address = Column(String(255))
    bloodGroup = Column(String(20))
   