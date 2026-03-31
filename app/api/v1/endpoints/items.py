from fastapi import APIRouter, Query

from app.schemas.item import Item, ItemIdParams


router = APIRouter(prefix="", tags=["items"])


@router.get("/items/{item_id}")
async def read_item(query: ItemIdParams = Query()):
    return {
        "item_id": query.item_id,
        "query_params": {
            "param1": query.param1,
            "param2": query.param2,
            "param3": query.param3,
        },
    }


@router.post("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> dict[str, str | int | bool | float | None]:
    return {"item_id": item_id, **item.model_dump()}


@router.patch("/items/{item_id}")
async def patch_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump(exclude_unset=True)}
