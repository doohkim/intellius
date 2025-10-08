import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


# 데이터베이스 설정
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_NAME = os.getenv("DATABASE_NAME", "intellius_chat")
DATABASE_USER = os.getenv("DATABASE_USER", "intellius")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "intellius123")

# MariaDB 연결 URL
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
ASYNC_DATABASE_URL = f"mysql+aiomysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# 동기 엔진
engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 비동기 엔진
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=64,
)

# 비동기 세션 팩토리
AsyncSessionFactory = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


def get_db():
    """동기 데이터베이스 세션"""
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


async def get_async_db():
    """비동기 데이터베이스 세션"""
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()
