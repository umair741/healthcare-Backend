from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_db
from tables import User, Doctor
from auth.schema import UserCreate, DoctorCreate, UserLogin, UserResponse
from auth.hash_pass import hash_password, verify_password
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------- USER SIGNUP ----------
@router.post("/signup/user", response_model=UserResponse)
async def signup_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # ✅ Check if email or national_id already exists
        result = await db.execute(select(User).where(User.email == user.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        result = await db.execute(select(User).where(User.national_id == user.national_id))
        existing_nid = result.scalars().first()
        if existing_nid:
            raise HTTPException(status_code=400, detail="National ID already registered")

        # ✅ Create new user
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

    except HTTPException:
        # Re-raise FastAPI-specific errors
        raise

    except SQLAlchemyError as e:
        # Rollback transaction if something goes wrong
        await db.rollback()
        print("❌ Database Error:", e)
        raise HTTPException(status_code=500, detail="Database error occurred. Please try again later.")


@router.post("/signup/doctor")
async def signup_doctor(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == doctor.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        national_id=doctor.national_id,
        name=doctor.name,
        dob=doctor.dob,
        gender=doctor.gender,
        email=doctor.email,
        phone=doctor.phone,
        address=doctor.address,
        password_hash=hash_password(doctor.password),
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

@router.get("/dashboard")
async def dashboard(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "name": db_user.name,
        "role": db_user.role
    }