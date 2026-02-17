from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from b_e.config import config



# Chuỗi kết nối async – dùng asyncpg
DATABASE_URL = config['DATABASE_URL']

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,                # Bật chế độ tương lai (tốt hơn)
    pool_pre_ping=True,
)

# Async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,          # optional nhưng tốt để rõ ràng
    expire_on_commit=False,       # tránh lazy load sau commit
)


async def get_db():
    async with async_session_factory() as session:
        yield session


async def test_db():
    print("Creating DB Connector")

    async with async_session_factory() as session:  # ← dùng factory
        result = await session.execute(text("SELECT version();"))
        version = result.scalar()
        print(f"PostgreSQL version: {version}")
        print("Database connected successfully!!!")


