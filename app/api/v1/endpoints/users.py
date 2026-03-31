from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import ActiveUserDep
from app.schemas.common import CommonQueryParams
from app.schemas.user import User


router = APIRouter(prefix="", tags=["users"])


@router.get("/users/", response_model=CommonQueryParams)
async def read_users(commons: Annotated[CommonQueryParams, Depends()]) -> CommonQueryParams:
    return commons


@router.get("/authorized", response_model=User)
async def read_authorized(current_user: ActiveUserDep) -> User:
    return current_user


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: ActiveUserDep) -> User:
    return current_user
