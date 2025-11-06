from app.core.models import Profile
from app.profiles.utils.schemas import (
    ProfileOut,
    ProfileResponse,
)


def convert_profiledb(profile: Profile) -> ProfileResponse:
    return ProfileResponse(
        name_img = profile.name_img,
        img = True,
        user_id = profile.user_id,
        id = profile.id,
    )


def convert_profiledb_to_out(profile: Profile) -> ProfileOut:
    return ProfileOut(
        name_img = profile.name_img,
        img = True,
        username = profile.user.username,
        user_id = profile.user_id,
    )
