from fastapi import APIRouter

from app.users.routers import admin, auth, me, registration

router = APIRouter()
router.include_router(registration.router)
router.include_router(auth.router)
router.include_router(me.router)
router.include_router(admin.router)
