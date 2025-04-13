import aio_pika
import asyncio
from aio_pika import RobustConnection, RobustChannel
from loguru import logger
from utils.rabbit_utils.wait_for_connection import wait_for_rabbitmq
from web.core.settings import settings


rabbitmq_connection: RobustConnection = None
rabbitmq_channel: RobustChannel = None


async def init_rabbitmq():
    global rabbitmq_connection, rabbitmq_channel

    # Ждём TCP доступности RabbitMQ
    wait_for_rabbitmq(
        settings.rabbit.rabbit_host,
        settings.rabbit.rabbit_port
    )

    # После TCP-доступности — пробуем подключиться через AMQP
    retries = 10
    while retries:
        try:
            rabbitmq_connection = await aio_pika.connect_robust(
                settings.rabbit.rabbit_url
            )
            rabbitmq_channel = await rabbitmq_connection.channel()
            logger.info("RabbitMQ connected successfully.")
            break
        except Exception as exc:
            retries -= 1
            logger.error(f"RABBITMQ UNAVAILABLE: {exc}. Retrying in 3 seconds...")
            await asyncio.sleep(3)
