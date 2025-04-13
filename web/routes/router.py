from fastapi import APIRouter

from web.routes.v1.routes import router as v1_router


router = APIRouter(prefix="/api")
router.include_router(v1_router)
