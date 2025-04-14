import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from web.routes.router import router
from web.core.db import Base, engine
from web.core.rabbit import init_rabbitmq, close_rabbitmq
from web.core.redis_ import init_redis, close_redis


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
            logger.error(f"DATABASE UNAVAILABLE: {exc}. Retrying in 3 seconds...")
            await asyncio.sleep(3)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing services...")

    await init_db()
    await init_rabbitmq()
    await init_redis()

    logger.info("All services initialized.")
    try:
        yield
    finally:
        logger.info("Shutting down services...")
        await close_rabbitmq()
        await close_redis()
        logger.info("All services shut down.")


app = FastAPI(
    lifespan=lifespan
)
app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
