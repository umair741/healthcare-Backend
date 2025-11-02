from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_db
from tables import User
from auth.schema import UserCreate, UserLogin, UserResponse
from auth.hash_pass import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        print("Password raw:", repr(user.password))
        print("Password type:", type(user.password))
        print("Password bytes length:", len(user.password.encode()))

        result = await db.execute(select(User).where(User.email == user.email))
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password)  # hash once
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except Exception as e:
        print("Signup error:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalars().first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": db_user.id}
