from sqlmodel import Field, Relationship, SQLModel

from app.models.item import UserItem


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, max_length=50)
    hashed_password: str
    disabled: bool = False
    email: str | None = Field(default=None, index=True)
    full_name: str | None = None
    items: list["UserItem"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
