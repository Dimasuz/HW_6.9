from aiohttp import web

from app import app
from models import Base, engine
from views import AdvView, UserView

routes = web.RouteTableDef()


@routes.get("/index/")
async def index(request):
    return web.Response(text="Hello, this is my homework from Flask to Aiohttp!")


async def orm_context(app: web.Application):
    print("START")
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    yield await engine.dispose()


app.cleanup_ctx.append(orm_context)


app.add_routes(
    [
        web.get("/users/{user_id:\d+}/", UserView),
        web.post("/users/", UserView),
        web.delete("/users/{user_id:\d+}/", UserView),
        web.get("/adv/{adv_id:\d+}/", AdvView),
        web.post("/adv/", AdvView),
        web.patch("/adv/{adv_id:\d+}/", AdvView),
        web.delete("/adv/{adv_id:\d+}/", AdvView),
        web.get("/", index),
    ]
)

if __name__ == "__main__":
    web.run_app(app, port=8000)
