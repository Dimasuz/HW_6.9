import json
from typing import Any, Dict, Optional, Type

from aiohttp import web
from pydantic import BaseModel, ValidationError, validate_arguments, validator

ERROR_TYPE = (
    Type[web.HTTPUnauthorized] | Type[web.HTTPForbidden] | Type[web.HTTPNotFound]
)


def raise_http_error(error_class: ERROR_TYPE, message: str | dict):
    raise error_class(
        text=json.dumps({"status": "error", "description": message}),
        content_type="application/json",
    )


class CreateAdv(BaseModel):
    title: str
    descr: str
    user_id: int
    password: str

    @validator("title")
    def check_title(cls, value: str):
        if len(value) > 50:
            raise_http_error(web.HTTPBadRequest, f'title: "{value}" is too long')
        return value

    @validator("descr")
    def check_descr(cls, value: str):
        if len(value) > 200:
            raise_http_error(web.HTTPBadRequest, f'descr: "{value}" is too long')
        return value


class PatchDelAdv(BaseModel):
    title: Optional[str]
    descr: Optional[str]
    user_id: int
    password: str

    @validator("title")
    def check_title(cls, value: str):
        if len(value) > 50:
            raise_http_error(web.HTTPBadRequest, f'title: "{value}" is too long')
        return value

    @validator("descr")
    def check_descr(cls, value: str):
        if len(value) > 200:
            raise_http_error(web.HTTPBadRequest, f'descr: "{value}" is too long')
        return value


SCHEMA_TYPE = Type[CreateAdv] | Type[PatchDelAdv]


@validate_arguments
async def validate(
    model_cls: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True
) -> dict:
    try:
        validated = model_cls(**data)
        return validated.dict(exclude_none=exclude_none)
    except ValidationError:
        raise_http_error(web.HTTPBadRequest, "wrong arguments in request")
