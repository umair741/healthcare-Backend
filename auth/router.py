from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_db
from tables import User, Doctor
from auth.schema import UserCreate, DoctorCreate, UserLogin, UserResponse
from auth.hash_pass import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------- USER SIGNUP ----------
@router.post("/signup/user", response_model=UserResponse)
async def signup_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if email or national_id already exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        national_id=user.national_id,
        name=user.name,
        dob=user.dob,
        gender=user.gender,
        email=user.email,
        phone=user.phone,
        address=user.address,
        password_hash=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/signup/doctor")
async def signup_doctor(user: UserCreate, doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        national_id=user.national_id,
        name=user.name,
        dob=user.dob,
        gender=user.gender,
        email=user.email,
        phone=user.phone,
        address=user.address,
        password_hash=hash_password(user.password),
        role="doctor"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Then create doctor profile
    new_doctor = Doctor(
        user_id=new_user.id,
        qualification=doctor.qualification,
        specialization=doctor.specialization,
        designation=doctor.designation,
        education=doctor.education,
        clinic_name=doctor.clinic_name,
        experience=doctor.experience,
    )
    db.add(new_doctor)
    await db.commit()

    return {"message": "Doctor signup successful", "user_id": new_user.id}


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalars().first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": db_user.id, "role": db_user.role}
