
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.services.user_service import SQLAlchemyUserRepository
from app.profiles.services.profile_service import ProfileService
from app.profiles.utils.dir import (
    clear_upload_dir,
)
from app.users.schemas import Token, UserLogin, UserResponse
from app.users.services.iuser_service import IUserService
from app.users.utils.checks import (
    check_for_auth,
    check_no_active,
)
from app.users.utils.send_email import send_email
from app.users.utils.token import (
    create_access_token,
    decode_jwt_email,
    update_token,
    build_auth_response,
)


class UserService(IUserService):

    # Registration
    async def create_user(self, session: AsyncSession, user: User) -> None:
        await SQLAlchemyUserRepository(session).add_user(user)
        await ProfileService().create_profile(session=session, user_id=user.id)
        send_email(user)

    async def registration_confirmation(self, session: AsyncSession, token: str) -> JSONResponse:
        email = await decode_jwt_email(token=token)
        user_db = await SQLAlchemyUserRepository(session).get_user_by_email(email)
        check_no_active(user_db)
        response = await build_auth_response(session=session, user_db=user_db)
        return response


    # Auth
    async def refresh_token(self, session: AsyncSession, refresh_token: str) -> Token:
        username = update_token(session,refresh_token)
        access_token = create_access_token({"sub": username})
        return Token(access_token=access_token,token_type="bearer")

    async def login_for_access(self, user: UserLogin, session: AsyncSession) -> JSONResponse:
        user_db = await SQLAlchemyUserRepository(session).get_user_by_username(user.username)
        check_for_auth(user_db,user_db.password)
        response = await build_auth_response(session=session, user_db=user_db)
        return response

    # Me
    async def delete_me_user(self, current_user: UserResponse, session: AsyncSession) -> None:
        user_db = await SQLAlchemyUserRepository(session).get_user_by_id(current_user.id)
        await SQLAlchemyUserRepository(session).delete_user(user_db)

    async def read_me_user(self, current_user: UserResponse) -> UserResponse:
        return current_user


    #Admin
    async def delete_all_users(self, session: AsyncSession) -> None:
        await SQLAlchemyUserRepository(session).delete_all_users()
        clear_upload_dir()

    async def dellete_all_no_comfirm_users(self, session: AsyncSession) -> None:
        await SQLAlchemyUserRepository(session).delete_no_comfirm_users()

    async def  get_user_by_id(self, user_id: int, session: AsyncSession) -> UserResponse:
        user_db = await SQLAlchemyUserRepository(session).get_user_by_id(user_id)
        if user_db is not None:
            return UserResponse.model_validate(user_db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
        )

    