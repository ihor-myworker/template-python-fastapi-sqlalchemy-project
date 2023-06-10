import pydantic


class BadRequestModel(pydantic.BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "BadRequest raised."},
        }
