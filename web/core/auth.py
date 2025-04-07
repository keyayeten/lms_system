from robyn import Request
from robyn.authentication import AuthenticationHandler, Identity

from utils.thread_utils.run_in_pool import run_async_in_thread
from core.db import async_session_maker
from core.security import decode_access_token
from services.users import get_user_by_username


class BasicAuthHandler(AuthenticationHandler):
    def authenticate(self, request: Request):
        token = self.token_getter.get_token(request)

        try:
            payload = decode_access_token(token)
            username = payload["sub"]
        except Exception:
            return

        user = run_async_in_thread(self._get_user(username))

        if not user:
            return

        return Identity(claims={"user": f"{user}"})

    async def _get_user(self, username: str):
        async with async_session_maker() as session:
            return await get_user_by_username(session, name=username)
