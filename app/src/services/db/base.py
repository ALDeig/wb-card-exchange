from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from app.settings import settings


class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase):  # noqa: D101
    pass


if not settings.SQLITE_DSN:
    err_message = "SQLITE_DSN not set"
    raise ValueError(err_message)
engine = create_async_engine(settings.SQLITE_DSN)
session_factory = async_sessionmaker(engine, expire_on_commit=False)
