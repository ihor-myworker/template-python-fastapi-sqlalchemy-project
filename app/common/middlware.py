import time
from typing import Any

from fastapi import Request


class ProcessTimeToHeader:
    def __init__(self) -> None:
        pass

    async def __call__(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        process_time = time.time() - start
        response.headers["X-Process-Time"] = str(process_time)
        return response


# also an option
async def add_process_time_to_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(process_time)
    return response
