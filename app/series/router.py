from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

import app.common.schemas as common_schemas
import app.series.crud as crud
import app.series.models as series_model
import app.series.schemas as schemas
from app.common.dependencies import CommonListQueryDeps
from app.database.utils import get_db_for_api
from app.user.utils import User, get_current_active_user

router = APIRouter()


@router.get("/series/", status_code=status.HTTP_200_OK)
async def get_series(
    common: CommonListQueryDeps, db=Depends(get_db_for_api)
) -> list[schemas.Series]:
    return crud.get_all_series(db)


@router.get("/series/{series_id}", status_code=status.HTTP_200_OK)
async def get_specific_series(
    series_id: int, db=Depends(get_db_for_api)
) -> schemas.Series:
    series = crud.get_series(db, series_id)
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Series not found"
        )
    return series


@router.post(
    "/series/",
    status_code=status.HTTP_201_CREATED,
)
async def create_series(
    series: schemas.SeriesCreate,
    user: User = Depends(get_current_active_user),
    db=Depends(get_db_for_api),
) -> schemas.SeriesCreateResponse:
    db_series = crud.create_series(db, series)
    return db_series


@router.patch(
    "/series/{series_id}",
    responses={
        200: {"model": schemas.Series},
        400: {"model": common_schemas.BadRequestModel},
    },
    status_code=status.HTTP_200_OK,
)
async def patch_specific_series(
    series_id: int,
    series: schemas.SeriesPatch,
    user: User = Depends(get_current_active_user),
    db=Depends(get_db_for_api),
) -> schemas.Series:
    series_to_update = crud.get_series(db, series_id)

    if not series_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Series not found",
        )

    updated_data = crud.update_series(db, series=series_to_update, series_update=series)

    return updated_data


@router.delete("/series/{series_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_series(
    series_id: int,
    user: User = Depends(get_current_active_user),
    db=Depends(get_db_for_api),
):
    series_to_delete = crud.get_series(db, series_id)
    if not series_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Series not found",
        )
    crud.delete_series(db, series_id)
    return None
