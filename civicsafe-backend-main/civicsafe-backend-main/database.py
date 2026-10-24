import ssl
from urllib.parse import parse_qs, urlsplit
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

# asyncpg does not accept libpq-only URL parameters such as sslmode.
db_url = settings.DATABASE_URL.split("?")[0]
sslmode = parse_qs(urlsplit(settings.DATABASE_URL).query).get("sslmode", ["require"])[0]

ssl_ctx = ssl.create_default_context()

engine = create_async_engine(
    db_url,
    echo=False,
    connect_args={"ssl": False if sslmode.lower() == "disable" else ssl_ctx},
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()