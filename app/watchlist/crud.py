from sqlalchemy.orm import Session

from . import models, schemas


def get_watchlist(db: Session, watchlist_id: int):
    return db.query(models.Watchlist).filter(models.Watchlist.id == watchlist_id).first()


def get_user_watchlists(db: Session, user_id: int):
    return db.query(models.Watchlist).filter(models.Watchlist.user_id == user_id).all()


def create_watchlist(db: Session, watchlist: schemas.WatchlistCreate, user_id: int):
    db_watchlist = models.Watchlist(user_id=user_id, title=watchlist.title)
    db.add(db_watchlist)
    db.commit()
    db.refresh(db_watchlist)
    return db_watchlist


def update_watchlist(db: Session, watchlist_id: int, watchlist: schemas.WatchlistUpdate):
    db_watchlist = (
        db.query(models.Watchlist).filter(models.Watchlist.id == watchlist_id).first()
    )
    if db_watchlist:
        for field, value in watchlist.dict().items():
            setattr(db_watchlist, field, value)
        db.commit()
        db.refresh(db_watchlist)
    return db_watchlist


def delete_watchlist(db: Session, watchlist_id: int):
    db_watchlist = (
        db.query(models.Watchlist).filter(models.Watchlist.id == watchlist_id).first()
    )
    if db_watchlist:
        db.delete(db_watchlist)
        db.commit()
    return db_watchlist


def get_watchlist_series(db: Session, watchlist_id: int, series_id: int):
    return (
        db.query(models.WatchlistSeries)
        .filter(
            models.WatchlistSeries.watchlist_id == watchlist_id,
            models.WatchlistSeries.series_id == series_id,
        )
        .first()
    )


def get_watchlist_series_by_id(db: Session, wl_series_id: int):
    return (
        db.query(models.WatchlistSeries)
        .filter(models.WatchlistSeries.id == wl_series_id)
        .first()
    )


def get_watchlist_series_by_watchlist(db: Session, watchlist_id: int):
    return (
        db.query(models.WatchlistSeries)
        .filter(models.WatchlistSeries.watchlist_id == watchlist_id)
        .all()
    )


def create_watchlist_series(db: Session, watchlist_id: int, series_id: int):
    db_wl_series = models.WatchlistSeries(watchlist_id=watchlist_id, series_id=series_id)
    db.add(db_wl_series)
    db.commit()
    db.refresh(db_wl_series)
    return db_wl_series


def delete_watchlist_series(db: Session, wl_series_id: int):
    db_wl_series = (
        db.query(models.WatchlistSeries)
        .filter(models.WatchlistSeries.id == wl_series_id)
        .first()
    )
    if db_wl_series:
        db.delete(db_wl_series)
        db.commit()
    return db_wl_series
