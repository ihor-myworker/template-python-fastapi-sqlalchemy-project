from typing import Annotated

from fastapi import Depends, Header, HTTPException

# functional approach:
# async def common_list_params(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}

# CommonListQueryDeps = Annotated[dict, Depends(common_list_params)]

# class-based approach:


class CommonListQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


CommonListQueryDeps = Annotated[
    CommonListQueryParams, Depends()
]  # same as Depends(CommonListQueryParams)


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "my_secret_key":
        raise HTTPException(status_code=400, detail="Invalid x-key")
    return x_key


async def verify_token(xyz_token: Annotated[str, Header()]):
    if xyz_token != "my_secret_token":
        raise HTTPException(status_code=400, detail="Invalid xyz-token")
