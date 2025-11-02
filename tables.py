
from sqlalchemy import Column, Integer, String
from db import Base, engine
import asyncio

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)


async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created successfully!")
    except Exception as e:
        print("❌ Error creating tables:")
        print(e)

# ✅ Run directly
if __name__ == "__main__":
    asyncio.run(create_tables())
