import pydantic


def reusable_validator(fields: list[str], validation_func: callable) -> classmethod:
    decorator = pydantic.validator(*fields, allow_reuse=True)
    validator = decorator(validation_func)
    return validator


def min_length(field_val, *, field):
    if len(field_val) < 1:
        raise ValueError(f"{field.name} can't be empty")
    return field_val

    # @validator("season", "episodes", "year")


def only_positive_numbers(field_val, *, field):
    if field_val < 0:
        raise ValueError(f"{field.name} can't be a negative number")
    return field_val
