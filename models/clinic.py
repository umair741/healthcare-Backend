from sqlalchemy import Column, String,TIMESTAMP
from db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
class clinic(Base):
    __tablename__ = "clinic"
    id = Column(UUID,default=uuid.uuid4,primary_key=True,index=True)
    name =Column(String(250),nullable=False)
    address = Column(String(500))
    phone = Column(String(24))
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),server_default=func.now())