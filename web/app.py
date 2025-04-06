import asyncio

from robyn import Robyn, logger
from core.db import Base, engine
from core.rabbit import init_rabbitmq
from core.settings import settings
from routes.router import router


app = Robyn(__file__)
app.include_router(router)


async def init_db():
    retries = 10
    while retries:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database connected and initialized successfully.")
            break
        except Exception as exc:
            retries -= 1
            logger.error(f"DATABASE UNAVAILAIBLE: {exc}. Retrying in 3 seconds...")
            await asyncio.sleep(3)


@app.get("/")
def index():
    return "Hello World!"


async def on_startup():
    await init_db()
    await init_rabbitmq()


app.startup_handler(on_startup)


if __name__ == "__main__":
    logger.info(f"application startup on host={settings.app.host}, port={settings.app.port}")
    app.start(host=settings.app.host, port=settings.app.port)
