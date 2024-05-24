from datetime import date

from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.src.services.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, primary_key=True, autoincrement=False
    )
    full_name: Mapped[str]
    username: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)


class Card(Base):
    __tablename__ = "cards"
    scu: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    last_posting_date: Mapped[date] 


class Settings(Base):
    __tablename__ = "settings"
    key: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[str] = mapped_column(Text)

