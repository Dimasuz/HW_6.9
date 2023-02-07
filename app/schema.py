from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, ValidationError, validator, validate_arguments

from errors import ApiError


class CreateAdv(BaseModel):
    title: str
    descr: str
    user_id: int
    password: str

    @validator("title")
    def check_title(cls, value: str):
        if len(value) > 60:
            raise ValueError(f"too long title - {len(value)}")
        return value

    @validator("descr")
    def check_descr(cls, value: str):
        if len(value) > 200:
            raise ValueError("too long descr")
        return value


class PatchDelAdv(BaseModel):
    title: Optional[str]
    descr: Optional[str]
    user_id: int
    password: str

    @validator("title")
    def check_title(cls, value: str):
        if len(value) > 50:
            raise ValueError("too long title")
        return value


SCHEMA_TYPE = Type[CreateAdv] | Type[PatchDelAdv]


@validate_arguments
async def validate(
    model_cls: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True
) -> dict:
    try:
        validated = model_cls(**data)
        return validated.dict(exclude_none=exclude_none)
    except ValidationError as er:
        raise ApiError(400, er.errors())
