from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class UserItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    price: float = Field(gt=0, description="Price must be greater than zero")
    owner_username: str = Field(foreign_key="user.username", index=True)
    owner: "User" = Relationship(back_populates="items")
