import json
from typing import Type

import bcrypt
from aiohttp import web

from models import Adv, Session, Users
from schema import CreateAdv, PatchDelAdv, raise_http_error, validate


async def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


async def get_item(
    session: Session, model_cls: Type[Users] | Type[Adv], item_id: int
) -> Users | Adv:
    item = await session.get(model_cls, item_id)
    if item is None:
        raise_http_error(web.HTTPNotFound, f"{model_cls.__name__.lower()} not found")
    return item


async def get_items(
    session: Session, model_cls: Type[Users] | Type[Adv]
) -> Users | Adv:
    items = session.query(model_cls).all()
    if items is None:
        raise_http_error(web.HTTPNotFound, f"{model_cls.__name__.lower()} not found")
    return items


async def check_user(session: Session, adv_user_id=0, **item_data):
    if "password" in item_data:
        user = await get_item(session, Users, item_data["user_id"])
        if adv_user_id == 0:
            adv_user_id = user.id
        if (
            bcrypt.checkpw(item_data["password"].encode(), user.password.encode())
            and adv_user_id == user.id
        ):
            item_data.pop("password")
            return item_data
        else:
            raise_http_error(web.HTTPUnauthorized, "wrong user_id or password")


class UserView(web.View):
    async def get(self):
        user_id = int(self.request.match_info["user_id"])
        async with Session() as session:
            user = await get_item(session, Users, user_id)
            return web.json_response(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                }
            )

    async def post(self):
        user_data = await self.request.json()
        user_data["password"] = await hash_password(user_data["password"])
        async with Session() as session:
            # user_data["password"] = await hash_password(user_data["password"])
            new_user = Users(**user_data)
            session.add(new_user)
            try:
                await session.commit()
            except web.HTTPConflict:
                raise_http_error(web.HTTPConflict, "User already exists")
        return web.json_response(
            {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
            }
        )

    async def delete(self):
        user_id = int(self.request.match_info["user_id"])
        async with Session() as session:
            user = await get_item(session, Users, user_id)
            await session.delete(user)
            await session.commit()
            return web.json_response({"id": user.id})


class AdvView(web.View):
    async def get(self):
        adv_id = int(self.request.match_info["adv_id"])
        async with Session() as session:
            adv = await get_item(session, Adv, adv_id)
        return web.json_response(
            {
                "id": adv.id,
                "title": adv.title,
                "descr": adv.descr,
                "creat_time": adv.creat_time.isoformat(),
                "user_id": adv.user_id,
            }
        )

    async def post(self):
        adv_data = await self.request.json()
        adv_data = await validate(CreateAdv, adv_data)
        async with Session() as session:
            adv_data = await check_user(session, **adv_data)
            new_adv = Adv(**adv_data)
            session.add(new_adv)
            await session.commit()
        return web.json_response({"id": new_adv.id})

    async def patch(self):
        adv_id = int(self.request.match_info["adv_id"])
        adv_data = await self.request.json()
        adv_data = await validate(PatchDelAdv, adv_data)
        async with Session() as session:
            adv = await get_item(session, Adv, adv_id)
            adv_data = await check_user(session, adv.user_id, **adv_data)
            for field, value in adv_data.items():
                setattr(adv, field, value)
            session.add(adv)
            await session.commit()
            return web.json_response({"id": adv.id, "descr": adv.descr})

    async def delete(self):
        adv_id = int(self.request.match_info["adv_id"])
        adv_data = await self.request.json()
        adv_data = await validate(PatchDelAdv, adv_data)
        async with Session() as session:
            adv = await get_item(session, Adv, adv_id)
            adv_data = await check_user(session, adv.user_id, **adv_data)
            await session.delete(adv)
            await session.commit()
            return web.json_response({"id": adv.id})
