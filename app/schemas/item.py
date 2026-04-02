from pydantic import BaseModel, ConfigDict, Field


class ItemCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(max_length=50)
    price: float = Field(gt=0, description="Price must be greater than zero")


class ItemPatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, max_length=50)
    price: float | None = Field(
        default=None,
        gt=0,
        description="Price must be greater than zero",
    )


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    owner_username: str
