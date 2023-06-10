from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from app.database.utils import Base


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String)
    description: Mapped[str] = Column(Text)
    season: Mapped[int] = Column(Integer)
    episodes: Mapped[int] = Column(Integer)
    year: Mapped[int] = Column(Integer)
    status: Mapped[str] = Column(String)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), onupdate=func.now())

    watchlist_series = relationship(
        "WatchlistSeries", back_populates="series", cascade="all, delete"
    )

    def __repr__(self):
        return f"<Series(id={self.id}, title='{self.title}', season={self.season}, episodes={self.episodes}, year={self.year})>"
