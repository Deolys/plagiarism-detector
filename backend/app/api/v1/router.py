from fastapi import APIRouter
from app.api.v1.endpoints import health, check

router = APIRouter(prefix="/api/v1")

router.include_router(health.router, tags=["health"])
router.include_router(check.router, tags=["plagiarism"])
