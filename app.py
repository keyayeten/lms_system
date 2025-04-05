from robyn import Robyn, logger
from core.db import Base, engine
from core.settings import settings
from routes.router import router


app = Robyn(__file__)
app.include_router(router)


@app.startup()
async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as exc:
        logger.error(f"DATABASE UNAVAILAIBLE: {exc}")


@app.get("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    logger.info(f"application startup on host={settings.app.host}, port={settings.app.port}")
    app.start(host=settings.app.host, port=settings.app.port)
