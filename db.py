# db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Database URL — change password/db name if needed
DATABASE_URL = "postgresql+asyncpg://postgres:umairmemon38#@localhost:5432/Healthcare"

# ✅ Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# ✅ Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ✅ Declare Base (all models will inherit this)
Base = declarative_base()

# ✅ Dependency for FastAPI (optional)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
