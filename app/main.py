from fastapi import FastAPI

import uvicorn

from users.views import router as users_router
from posts.views import router as posrs_router
from profiles.views import router as profile_router



app=FastAPI()
app.include_router(users_router, tags=["Users"]) 
app.include_router(posrs_router, tags=["Posts"]) 
app.include_router(profile_router, tags=["Profile"])

if __name__=="__main__":
    uvicorn.run("main:app",reload=True)
    
    
    # poetry run python app/main.py