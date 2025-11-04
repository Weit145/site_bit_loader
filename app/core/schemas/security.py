from pydantic import BaseModel

class Cookies(BaseModel):
    key:str
    value:str
    httponly:bool = False
    secure: bool = True
    samesite:str = "strict"
    max_age :int = 7*24*3600


# response.set_cookie(
#     key="refresh_token",
#     value=refresh_token,
#     httponly=True,    # 🔒 нельзя прочитать из JS
#     secure=True,      # 🚫 не уходит по HTTP, только HTTPS
#     samesite="Strict",# 🛡️ не отправляется с других сайтов (CSRF защита)
#     max_age=7 * 24 * 3600
# )
