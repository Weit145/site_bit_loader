import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.posts import router as posts_router
from app.profiles import router as profile_router
from app.users import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router,prefix="/user", tags=["Users"])
app.include_router(posts_router,prefix="/post", tags=["Posts"])
app.include_router(profile_router,prefix="/profile", tags=["Profile"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

    # poetry run python app/main.py
    # docker compose up --build
