from pydantic import BaseModel, EmailStr, Field


class Item(BaseModel):
    name: str = Field(max_length=50)
    price: float = Field(gt=0, description="Price must be greater than zero")
    is_offer: bool | None = None
    email: EmailStr


class ItemIdParams(BaseModel):
    item_id: int = Field(..., description="The ID of the item to retrieve")
    param1: str | None = Field(
        None,
        min_length=3,
        max_length=50,
        description="A query parameter with a minimum length of 3 and a maximum length of 50",
    )
    param2: str | None = None
    param3: int = Field(..., description="A required integer query parameter")
