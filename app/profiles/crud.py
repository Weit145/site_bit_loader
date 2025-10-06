from fastapi import Depends, HTTPException, status

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from .schemas import CreateProfile,ProfileResponse,ProfileBase
from core.models import Profile

async def create_profile(
    session:AsyncSession,
    profile_create:CreateProfile,
)->ProfileResponse:
    profile=Profile(**profile_create.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return ProfileResponse.model_validate(profile)