from robyn import SubRouter

from routes.v1.routes import router as v1_router


router = SubRouter(__file__, prefix="/api")
router.include_router(v1_router)
