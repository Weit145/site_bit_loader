from fastapi import APIRouter

from app.profiles.routers import admin, me

router = APIRouter()
router.include_router(me.router)
router.include_router(admin.router)
