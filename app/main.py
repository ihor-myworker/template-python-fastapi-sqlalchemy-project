from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

import app.series.router as series_router
import app.user.router as user_router
import app.watchlist.router as watchlist_router
from app.common.middlware import ProcessTimeToHeader

app = FastAPI()

# global dependencies
# app = FastAPI(dependencies=[
#         Depends(verify_key),
#         Depends(verify_token),
#     ],)

process_time_to_header = ProcessTimeToHeader()
app.add_middleware(BaseHTTPMiddleware, dispatch=process_time_to_header)

app.include_router(series_router.router, tags=["Series"])
app.include_router(user_router.router, tags=["User"])
app.include_router(watchlist_router.router, tags=["Watchlist"])


@app.get("/")
async def root():
    return {"message": "Remwatch is alive"}
