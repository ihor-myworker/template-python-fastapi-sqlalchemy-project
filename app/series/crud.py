from sqlalchemy.orm import Session

import app.series.models as models
import app.series.schemas as schemas


def get_series(db: Session, series_id: int):
    return (
        db.query(models.Series)
        .filter(
            models.Series.id == series_id,
        )
        .first()
    )


def get_all_series(db: Session):
    return db.query(models.Series).all()


def create_series(db: Session, series: schemas.SeriesCreate):
    db_series = models.Series(**series.dict())
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series


def update_series(db: Session, series: models.Series, series_update: schemas.SeriesPatch):
    for field, value in series_update.dict().items():
        if value is not None:
            setattr(series, field, value)

    db.commit()
    db.refresh(series)
    return series


def delete_series(db: Session, series_id: int):
    db_series = db.query(models.Series).filter(models.Series.id == series_id).first()

    if db_series:
        db.delete(db_series)
        db.commit()
    return db_series
