from robyn import Robyn
from core.db import Base, engine
from routes.router import router


app = Robyn(__file__)
app.include_router(router)


@app.startup()
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
