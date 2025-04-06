from robyn import SubRouter

from routes.v1.users import users as users_route


router = SubRouter(__file__, prefix="/v1")

router.include_router(users_route)
