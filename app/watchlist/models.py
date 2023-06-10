from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from app.database.utils import Base
from app.series.models import Series
from app.user.models import User


class Watchlist(Base):
    __tablename__ = "watchlist"

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = Column(String)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship(User, back_populates="watchlist")
    watchlist_series = relationship(
        "WatchlistSeries", back_populates="watchlist", cascade="all, delete"
    )

    def __repr__(self):
        return f"<Watchlist(id={self.id}, user_id={self.user_id}, series_id={self.series_id})>"


class WatchlistSeries(Base):
    __tablename__ = "watchlist_series"

    id: Mapped[int] = Column(Integer, primary_key=True)
    watchlist_id: Mapped[int] = Column(Integer, ForeignKey("watchlist.id"))
    series_id: Mapped[int] = Column(Integer, ForeignKey("series.id"))

    watchlist = relationship(Watchlist, back_populates="watchlist_series")
    series = relationship(Series, back_populates="watchlist_series")

    def __repr__(self):
        return f"<WatchlistSeries(id={self.id}, watchlist_id={self.watchlist_id}, series_id={self.series_id})>"
