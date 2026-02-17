from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

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
        try:
            yield session
        finally:
            await session.close()


async def test_db():
    print("Creating DB Connector")

    async with async_session_factory() as session:  # ← dùng factory
        try:
            result = await session.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"PostgreSQL version: {version}")
            print("Database connected successfully!!!")
        except Exception as e:
            print(f"Error reason: {e}")
            print("Error connecting to database")


async def init_database():
        # Lấy tên database từ URL
        db_url_parts = DATABASE_URL.split("/")
        db_name = db_url_parts[-1]

        default_db_url = "/".join(db_url_parts[:-1]) + "/postgres"

        temp_engine = create_async_engine(
            default_db_url,
            isolation_level="AUTOCOMMIT",  # cần cho CREATE DATABASE
            echo=False,  # tắt echo cho temp để sạch log
        )

        async with temp_engine.connect() as conn:
            try:
                # Kiểm tra tồn tại (dùng query an toàn)
                result = await conn.execute(
                    text(f"SELECT 1 FROM pg_database WHERE datname = :db_name"),
                    {"db_name": db_name}
                )
                exists = result.scalar() is not None

                if not exists:
                    print(f"Database '{db_name}' không tồn tại → đang tạo...")
                    await conn.execute(text(f"CREATE DATABASE {db_name}"))
                    print(f"Database '{db_name}' đã được tạo thành công!")
                else:
                    print(f"Database '{db_name}' đã tồn tại.")
            except Exception as e:
                print(f"Lỗi khi kiểm tra/tạo database: {e}")
                raise

        await temp_engine.dispose()

class Base(DeclarativeBase):
    pass



