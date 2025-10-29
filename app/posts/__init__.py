from fastapi import APIRouter

from app.posts.routers import admin, post

router = APIRouter()
router.include_router(post.router)
router.include_router(admin.router)
