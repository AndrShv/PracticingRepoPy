from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from workspace.configs.main_config import settings
import asyncio

_async_engine = None
_session_factory = None
_db_initialized = False
_db_init_lock = asyncio.Lock()

class Base(DeclarativeBase):
    pass




class DbConnection:
    _saved = None
    _init_done = False


    def __new__(cls, *args, **kwargs):
        if cls._saved is None:
            cls._saved = super().__new__(cls)
        return cls._saved

    def __init__(self, user: str = "", password: str = "", server: str = "", port: int = 0, db_name: str = "",):
        if DbConnection._init_done:
            return
        self.user = user
        self.password = password
        self.server = server
        self.port = port
        self.db_name = db_name
        DbConnection._init_done = True

    def _get_session_factory(self):
        global _async_engine, _session_factory
        if _session_factory is None:
            connect_args = {"statement_cache_size": 0}
            if settings.POSTGRES_SERVER not in {"localhost", "127.0.0.1", "postgres", "shop-postgres", "ml-postgres"}:
                connect_args["ssl"] = "require"

            _async_engine = create_async_engine(
                settings.database_url,
                echo=settings.DEBUG,
                pool_size=10,
                max_overflow=20,
                connect_args=connect_args,
            )
            _session_factory = async_sessionmaker(
                bind=_async_engine,
                class_=AsyncSession,
                autoflush=False,
                expire_on_commit=False,
            )
        return _session_factory

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._get_session_factory()() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def init_db(self):
        global _db_initialized

        if _db_initialized:
            return

        async with _db_init_lock:
            if _db_initialized:
                return

            self._get_session_factory()
            async with _async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            _db_initialized = True
