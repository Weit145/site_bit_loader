from app.core.models import User
from app.users.schemas import UserCreate
from app.users.utils.password import get_password_hash


def convert_profiledb(user: UserCreate)->User:
    user_db=User(
        username = user.username,
        password = get_password_hash(user.password),
        email = user.email,
    )
    return user_db
