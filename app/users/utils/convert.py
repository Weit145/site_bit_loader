from app.core.models import User
from app.core.security.password import get_password_hash
from app.users.utils.schemas import UserCreate

def convert_profiledb(user: UserCreate)->User:
    user_db=User(
        username = user.username,
        password = get_password_hash(user.password),
        email = user.email,
    )
    return user_db
