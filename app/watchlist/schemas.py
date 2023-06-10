from datetime import datetime

from pydantic import BaseModel

from app.common.schema_validators import min_length, reusable_validator
from app.series.schemas import Series
from app.user.schemas import User


class WatchlistBase(BaseModel):
    user_id: int
    title: str

    class Config:
        orm_mode = True


class Watchlist(WatchlistBase):
    id: int
    user_id: int
    title: str

    created_at: datetime = datetime.today()
    updated_at: datetime | None = datetime.today()


class WatchlistSeriesBase(BaseModel):
    watchlist_id: int
    series_id: int

    class Config:
        orm_mode = True


class WatchlistSeriesCreate(WatchlistSeriesBase):
    watchlist_id: int
    series_id: int

    class Config:
        orm_mode = True


class WatchlistSeriesInfo(BaseModel):
    watchlist_id: int
    series: Series

    class Config:
        orm_mode = True


class WatchlistFull(BaseModel):
    id: int
    title: str
    user: User
    watchlist_series: list[WatchlistSeriesInfo]
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class WatchlistCreate(BaseModel):
    title: str
    _title_min_length = reusable_validator(["title"], min_length)


class WatchlistCreateResponse(BaseModel):
    id: int
    title: str
    username: str
    created_at: datetime = datetime.today()

    class Config:
        orm_mode = True


class WatchlistUpdate(WatchlistCreate):
    pass


class WatchlistSeriesFull(BaseModel):
    watchlist: Watchlist
    series: Series

    class Config:
        orm_mode = True
