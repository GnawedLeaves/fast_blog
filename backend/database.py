from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# prevents problems with expired objects after a commit
AsyncSessionLocal = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)
                                      


class Base(DeclarativeBase):
    pass


# dependency functions that provides session to our routes. session acts as context manager to clean up
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
