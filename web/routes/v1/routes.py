from fastapi import APIRouter

from web.routes.v1.users import users as users_route
from web.routes.v1.auth import auth as auth_route


router = APIRouter(prefix="/v1")

router.include_router(users_route)
router.include_router(auth_route)
