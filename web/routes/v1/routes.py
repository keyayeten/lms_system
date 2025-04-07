from robyn import SubRouter

from routes.v1.users import users as users_route
from routes.v1.auth import auth as auth_route


router = SubRouter(__file__)

router.include_router(users_route)
router.include_router(auth_route)
