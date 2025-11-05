from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from db import Base, engine
import asyncio
import enum


# -------- ENUM CLASSES --------
class GenderEnum(enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class RoleEnum(enum.Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"
    assistant = "assistant"
    doctor_admin = "doctor_admin"


# -------- USERS TABLE --------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    national_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    dob = Column(Date)
    gender = Column(Enum(GenderEnum))
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    address = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(TIMESTAMP)

    doctor = relationship("Doctor", back_populates="user", uselist=False)


# -------- DOCTORS TABLE --------
class Doctor(Base):
    __tablename__ = "doctors"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    qualification = Column(String(255))
    specialization = Column(String(255))
    designation = Column(String(255))
    education = Column(String(255))
    clinic_name = Column(String(255))
    experience = Column(Integer)

    user = relationship("User", back_populates="doctor")


# -------- CREATE TABLES FUNCTION --------
async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created successfully!")
    except Exception as e:
        print("❌ Error creating tables:")
        print(e)


if __name__ == "__main__":
    asyncio.run(create_tables())
