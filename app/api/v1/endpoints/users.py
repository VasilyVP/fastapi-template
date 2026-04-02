from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import SessionDep, get_current_user
from app.repositories.user_repository import user_repository
from app.schemas.common import CommonQueryParams
from app.schemas.user import UserRead


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)

CurrentUser = Annotated[UserRead, Depends(get_current_user)]


@router.get("/", response_model=list[UserRead])
async def read_users(
    commons: Annotated[CommonQueryParams, Depends()],
    session: SessionDep,
) -> list[UserRead]:
    users = await user_repository.list_users(
        session,
        query=commons.q,
        skip=commons.skip,
        limit=commons.limit,
    )
    return [UserRead.model_validate(user) for user in users]


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: CurrentUser) -> UserRead:
    return current_user
