from random import random
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import Settings, get_settings
from app.schemas.common import InfoResponse, ModelName, RootResponse


router = APIRouter(prefix="", tags=["system"])


@router.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(hello="World")


@router.get("/info", response_model=InfoResponse)
async def info(settings: Annotated[Settings, Depends(get_settings)]) -> InfoResponse:
    return InfoResponse(
        app_name=settings.app_name,
        admin_email=settings.admin_email,
        items_per_user=settings.items_per_user,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )


@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


@router.get("/exception")  # , tags=["exception"]
async def raise_exception():
    if random() < 0.5:
        raise HTTPException(status_code=400, detail="This is a test HTTP exception")
    raise RuntimeError("This is a test exception")
