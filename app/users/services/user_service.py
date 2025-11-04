
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.security.file import (
    clear_upload_dir,
)
from app.core.security.token import (
    build_auth_response,
    create_access_token,
    decode_jwt_email,
    valid_refresh_token,
)
from app.core.services.user_service import SQLAlchemyUserRepository
from app.users.services.iuser_service import IUserService
from app.users.utils.checks import (
    check_for_auth,
    check_no_active,
    check_user_by_id,
)
from app.users.utils.convert import (
    convert_user_to_out,
)
from app.users.utils.schemas import (
    OutUser,
    Token,
    UserLogin,
)
from app.users.utils.send_email import send_email


class UserService(IUserService):

    # Registration
    async def create_user(self, session: AsyncSession, user: User) -> None:
        await SQLAlchemyUserRepository(session).add_user(user)
        send_email(user)

    async def registration_confirmation(self, session: AsyncSession, token: str) -> JSONResponse:
        email = await decode_jwt_email(token=token)
        user_db = await SQLAlchemyUserRepository(session).get_user_by_email(email)
        check_no_active(user_db)
        response = await build_auth_response(session=session, user_db=user_db)
        return response


    # Auth
    async def refresh_token(self, session: AsyncSession, refresh_token: str) -> Token:
        username = valid_refresh_token(session,refresh_token)
        access_token = create_access_token({"sub": username})
        return Token(access_token=access_token,token_type="bearer")

    async def authenticate_user(self, user: UserLogin, session: AsyncSession) -> JSONResponse:
        user_db = await SQLAlchemyUserRepository(session).get_user_by_username(user.username)
        check_for_auth(user_db,user_db.password)
        response = await build_auth_response(session=session, user_db=user_db)
        return response

    # Me
    async def delete_me_user(self, current_user: User, session: AsyncSession) -> None:
        await SQLAlchemyUserRepository(session).delete_user(current_user)

    async def read_me_user(self, current_user: User) -> OutUser:
        return convert_user_to_out(current_user)


    #Admin
    async def delete_all_users(self, session: AsyncSession) -> None:
        await SQLAlchemyUserRepository(session).delete_all_users()
        clear_upload_dir()

    async def dellete_all_no_comfirm_users(self, session: AsyncSession) -> None:
        await SQLAlchemyUserRepository(session).delete_no_comfirm_users()

    async def  get_user_by_id(self, user_id: int, session: AsyncSession) -> OutUser:
        user_db = await SQLAlchemyUserRepository(session).get_user_by_id(user_id)
        check_user_by_id(user_db, user_id)
        return convert_user_to_out(user_db)


