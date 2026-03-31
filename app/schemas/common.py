from enum import Enum

from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class CommonQueryParams(BaseModel):
    q: str | None = None
    skip: int = 0
    limit: int = 100


class RootResponse(BaseModel):
    hello: str


class InfoResponse(BaseModel):
    app_name: str
    admin_email: str | None = None
    items_per_user: int
    algorithm: str
    access_token_expire_minutes: int
