from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import uvicorn

from users.views import router as users_router

import os
from dotenv import load_dotenv

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
app=FastAPI()
app.include_router(users_router,tags=["Users"])


if __name__=="__main__":
    uvicorn.run("main:app",reload=True)
    
    
    # poetry run python app/main.py