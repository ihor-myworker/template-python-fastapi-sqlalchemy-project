from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

import app.watchlist.crud as crud
import app.watchlist.models as watchlist_models
import app.watchlist.schemas as watchlist_schema
from app.database.utils import get_db_for_api
from app.user.utils import User, get_current_active_user

router = APIRouter()


@router.get("/watchlist/my", response_model=list[watchlist_schema.WatchlistFull])
async def get_my_watchlist(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db=Depends(get_db_for_api),
):
    wl = crud.get_user_watchlists(db, current_user.id)
    return wl


@router.post("/watchlist/", response_model=watchlist_schema.WatchlistCreateResponse)
async def create_my_watchlist(
    watchlist: watchlist_schema.WatchlistCreate,
    user=Depends(get_current_active_user),
    db=Depends(get_db_for_api),
):
    db_watchlist = crud.create_watchlist(db, watchlist, user.id)
    return watchlist_schema.WatchlistCreateResponse(
        **db_watchlist.__dict__, username=user.username
    )


@router.put("/watchlist/{watchlist_id}", response_model=watchlist_schema.WatchlistFull)
async def update_watchlist(
    watchlist_id: int,
    watchlist: watchlist_schema.WatchlistUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db=Depends(get_db_for_api),
):
    db_watchlist = crud.get_watchlist(db, watchlist_id)
    if not db_watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist not found"
        )

    if db_watchlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this watchlist",
        )

    updated_wl = crud.update_watchlist(db, watchlist_id, watchlist)

    return updated_wl


@router.delete("/watchlist/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_watchlist(
    watchlist_id: int,
    user: User = Depends(get_current_active_user),
    db=Depends(get_db_for_api),
):
    watchlist_to_delete = crud.get_watchlist(db, watchlist_id)
    if not watchlist_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist not found"
        )
    if watchlist_to_delete.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this watchlist",
        )
    crud.delete_watchlist(db, watchlist_id)

    return None


@router.post("/watchlist_series/", response_model=watchlist_schema.WatchlistSeriesCreate)
async def add_series_to_watchlist(
    series_to_wl: watchlist_schema.WatchlistSeriesCreate,
    db=Depends(get_db_for_api),
):
    wl_series_exists = crud.get_watchlist_series(
        db, watchlist_id=series_to_wl.watchlist_id, series_id=series_to_wl.series_id
    )
    if wl_series_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Series already in this watchlist",
        )

    db_wl_series = crud.create_watchlist_series(
        db, watchlist_id=series_to_wl.watchlist_id, series_id=series_to_wl.series_id
    )
    return db_wl_series


@router.delete("/watchlist_series/{series_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_series_from_watchlist(
    series_id: int,
    user: User = Depends(get_current_active_user),
    db=Depends(get_db_for_api),
):
    series_to_delete = crud.get_watchlist_series_by_id(db, series_id)
    if not series_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Series not found"
        )

    crud.delete_watchlist_series(db, series_id)
    return None


@router.get(
    "/watchlist_series/my", response_model=list[watchlist_schema.WatchlistSeriesFull]
)
async def get_my_all_my_series_to_watch(
    user: User = Depends(get_current_active_user),
    db=Depends(get_db_for_api),
):
    watchlists = crud.get_user_watchlists(db, user.id)
    wl_series = []
    for wl in watchlists:
        wl_series += crud.get_watchlist_series_by_watchlist(db, wl.id)
    return wl_series
