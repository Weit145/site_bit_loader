from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import uvicorn

from passlib.context import CryptContext

from users.views import router as users_router
from posts.views import router as posrs_router

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
app=FastAPI()
app.include_router(users_router, tags=["Users"]) 
app.include_router(posrs_router, tags=["Posts"]) 

if __name__=="__main__":
    uvicorn.run("main:app",reload=True)
    
    
    # poetry run python app/main.py