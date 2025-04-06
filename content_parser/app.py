from faststream import FastStream
from faststream.rabbit import RabbitBroker
from sqlalchemy import text
from core.settings import settings
from core.db import engine

from utils.rabbit_utils.wait_for_connection import wait_for_rabbitmq


rabbit_host = settings.rabbit.rabbit_host
rabbit_port = settings.rabbit.rabbit_port


async def wait_for_database():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise


async def startup():
    wait_for_rabbitmq(rabbit_host, rabbit_port)
    await wait_for_database()

# === FastStream App ===

broker = RabbitBroker(settings.rabbit.rabbit_url)
app = FastStream(broker)


@app.on_startup
async def on_startup():
    await startup()


@broker.subscriber("test")
async def base_handler(body):
    print(f"📥 Received message: {body}")
