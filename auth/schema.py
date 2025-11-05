from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    national_id: str
    name: str
    dob: date
    gender: str         
    email: EmailStr
    phone: str
    address: str
    password: str
    role: str           


class UserResponse(BaseModel):
    id: int
    national_id: str
    name: str
    dob: date
    gender: str
    email: EmailStr
    phone: str
    address: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


    class Config:
        orm_mode = True

class DoctorCreate(BaseModel):
    user_id: int
    qualification: str
    specialization: str
    designation: str
    education: str
    clinic_name: str
    experience: int


class DoctorResponse(DoctorCreate):
    pass
