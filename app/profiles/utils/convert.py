from app.core.models import Profile
from app.profiles.schemas import ProfileResponse


def convert_profiledb(profile: Profile)->ProfileResponse:
    return ProfileResponse.model_validate(profile)
