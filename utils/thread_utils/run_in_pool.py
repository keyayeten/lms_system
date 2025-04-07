import asyncio
from threading import Thread


def run_async_in_thread(coro):
    result = {}

    def runner():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result["value"] = loop.run_until_complete(coro)
        except Exception as e:
            result["error"] = e

    thread = Thread(target=runner)
    thread.start()
    thread.join()

    if "error" in result:
        raise result["error"]

    return result["value"]
