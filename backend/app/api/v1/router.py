from fastapi import APIRouter
from app.api.v1.endpoints import health, check, upload

router = APIRouter(prefix="/api/v1")

router.include_router(health.router, tags=["health"])
router.include_router(check.router, tags=["plagiarism"])
router.include_router(upload.router, tags=["plagiarism"])
