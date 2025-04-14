import json
from web.core.rabbit import publish_message


class RabbitService:
    @staticmethod
    async def send_user_created(user_id: int, email: str):
        data = {
            "event": "user_created",
            "user_id": user_id,
            "email": email
        }

        await publish_message(
            routing_key="users.created",
            body=json.dumps(data).encode()
        )
