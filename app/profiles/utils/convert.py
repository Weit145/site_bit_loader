from app.core.models import Profile
from app.profiles.utils.schemas import (
    ProfileOut,
    ProfileResponse,
)


def convert_profiledb(profile: Profile) -> ProfileResponse:
    return ProfileResponse.model_validate(profile)


def convert_profiledb_to_out(profile: Profile) -> ProfileOut:
    return ProfileOut.model_validate(profile)
