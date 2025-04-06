import os

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from utils.rabbit_utils.wait_for_connection import wait_for_rabbitmq


rabbit_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
rabbit_port = int(os.getenv("RABBITMQ_PORT", 5672))

wait_for_rabbitmq(rabbit_host, rabbit_port)

# === FastStream App ===

broker = RabbitBroker(f"amqp://guest:guest@{rabbit_host}:{rabbit_port}/")
app = FastStream(broker)


@broker.subscriber("test")
async def base_handler(body):
    print(f"📥 Received message: {body}")
