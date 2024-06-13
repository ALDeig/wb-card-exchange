from datetime import date

from sqlalchemy import BigInteger, Date, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.src.services.date_utils import utc_date
from app.src.services.db.base import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, init=False, primary_key=True, autoincrement=False
    )
    full_name: Mapped[str]
    username: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    last_active: Mapped[date] = mapped_column(
        Date, default=utc_date
    )


class Card(Base):
    """Модель карточек, которые уже были запосчены на канал и дата последного поста."""

    __tablename__ = "cards"

    scu: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    last_posting_date: Mapped[date]


class Settings(Base):
    """Модель изменяемых настроек. Например приветственное сообщение."""

    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[str] = mapped_column(Text)


