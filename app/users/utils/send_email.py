from app.core.models import User
from app.core.security.token import create_access_token
from app.core.tasks.email.email import send_message


def send_email(user:User)->None:
    access_token = create_access_token(data={"sub": user.email})
    send_message.delay(token=access_token,username=user.username,email=user.email)
