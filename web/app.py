import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from web.routes.router import router
from web.core.db import Base, engine
from web.core.rabbit import init_rabbitmq


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


@asynccontextmanager
async def lifespan(span: FastAPI):
    await init_db()
    await init_rabbitmq()
    yield


app = FastAPI(
    lifespan=lifespan
)
app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
