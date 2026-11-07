from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(2048), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    source: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(100))

    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    external_id: Mapped[str | None] = mapped_column(String(2048))
    image_url: Mapped[str | None] = mapped_column(String(2048))