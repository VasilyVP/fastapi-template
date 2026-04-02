from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import SessionDep, get_current_user
from app.repositories.item_repository import item_repository
from app.schemas.common import CommonQueryParams
from app.schemas.item import ItemCreateRequest, ItemPatchRequest, ItemRead
from app.schemas.user import UserRead


router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_current_user)],
)

CurrentUser = Annotated[UserRead, Depends(get_current_user)]


def _item_not_found(item_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item {item_id} not found",
    )


@router.get("/", response_model=list[ItemRead])
async def read_items(
    commons: Annotated[CommonQueryParams, Depends()],
    current_user: CurrentUser,
    session: SessionDep,
) -> list[ItemRead]:
    items = await item_repository.list_items(
        session,
        owner_username=current_user.username,
        query=commons.q,
        skip=commons.skip,
        limit=commons.limit,
    )
    return [ItemRead.model_validate(item) for item in items]


@router.get("/{item_id}", response_model=ItemRead)
async def read_item(
    item_id: int,
    current_user: CurrentUser,
    session: SessionDep,
) -> ItemRead:
    item = await item_repository.get_item(
        session,
        item_id=item_id,
        owner_username=current_user.username,
    )
    if item is None:
        raise _item_not_found(item_id)

    return ItemRead.model_validate(item)


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreateRequest,
    current_user: CurrentUser,
    session: SessionDep,
) -> ItemRead:
    created_item = await item_repository.create_item(
        session,
        owner_username=current_user.username,
        name=item.name,
        price=item.price,
    )
    return ItemRead.model_validate(created_item)


@router.put("/{item_id}", response_model=ItemRead)
@router.post("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int,
    item: ItemCreateRequest,
    current_user: CurrentUser,
    session: SessionDep,
) -> ItemRead:
    existing_item = await item_repository.get_item(
        session,
        item_id=item_id,
        owner_username=current_user.username,
    )
    if existing_item is None:
        raise _item_not_found(item_id)

    updated_item = await item_repository.replace_item(
        session,
        item=existing_item,
        name=item.name,
        price=item.price,
    )
    return ItemRead.model_validate(updated_item)


@router.patch("/{item_id}", response_model=ItemRead)
async def patch_item(
    item_id: int,
    item: ItemPatchRequest,
    current_user: CurrentUser,
    session: SessionDep,
) -> ItemRead:
    existing_item = await item_repository.get_item(
        session,
        item_id=item_id,
        owner_username=current_user.username,
    )
    if existing_item is None:
        raise _item_not_found(item_id)

    updates = item.model_dump(exclude_unset=True)
    if not updates:
        return ItemRead.model_validate(existing_item)

    updated_item = await item_repository.patch_item(
        session,
        item=existing_item,
        updates=updates,
    )
    return ItemRead.model_validate(updated_item)
