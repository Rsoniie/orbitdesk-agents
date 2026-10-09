import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config.log_config import logger


load_dotenv("app/.env")
DATABASE_URL = os.getenv("NEON_CONNECTION_STRING")

if not DATABASE_URL:
    raise RuntimeError("NEON_CONNECTION_STRING is missing from app/.env")

DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": True},
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    return SessionLocal()



async def check_database_connection():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            if result.scalar() == 1:
                logger.info("Database connection successful.")
    except Exception:
        logger.exception("Database connection failed.")
        raise

