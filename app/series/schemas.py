from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from app.common.schema_validators import (
    min_length,
    only_positive_numbers,
    reusable_validator,
)


class SeriesStatus(str, Enum):
    planned = "Planned"
    in_production = "In Production"
    ended = "Ended"
    canceled = "Canceled"
    pilot = "Pilot"
    ongoing = "Ongoing"
    suspended = "Suspended"


class SeriesBase(BaseModel):
    id: int
    title: str
    description: str
    season: int
    episodes: int
    year: int
    status: SeriesStatus

    class Config:
        orm_mode = True


class Series(SeriesBase):
    created_at: datetime = datetime.today()
    updated_at: datetime | None = datetime.today()


class SeriesCreate(BaseModel):
    title: str
    description: str
    season: int
    episodes: int
    year: int
    status: SeriesStatus

    _titles_length_validation = reusable_validator(["title", "description"], min_length)
    _positive_nums_validation = reusable_validator(
        ["season", "episodes", "year"], only_positive_numbers
    )


class SeriesCreateResponse(SeriesBase):
    created_at: datetime = datetime.today()


class SeriesPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    season: int | None = None
    episodes: int | None = None
    year: int | None = None
    status: SeriesStatus | None = None

    _titles_length_validation = reusable_validator(["title", "description"], min_length)
    _positive_nums_validation = reusable_validator(
        ["season", "episodes", "year"], only_positive_numbers
    )
