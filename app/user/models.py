from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.database.utils import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    username: Mapped[str] = Column(String, index=True, unique=True)
    password: Mapped[str] = Column(String)

    # Define the one-to-many relationship with Watchlist
    watchlist = relationship("Watchlist", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
