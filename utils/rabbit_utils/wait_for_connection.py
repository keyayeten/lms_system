import time
import socket


def wait_for_rabbitmq(host: str, port: int, retries: int = 30, delay: int = 2):
    print(f"🔄 Waiting for RabbitMQ at {host}:{port}...")
    for i in range(retries):
        try:
            with socket.create_connection((host, port), timeout=3):
                print("✅ RabbitMQ is available!")
                return
        except OSError as e:
            print(f"Attempt {i + 1}/{retries} failed: {e}")
            time.sleep(delay)
    print("❌ RabbitMQ is still not reachable, exiting.")
    exit(1)
