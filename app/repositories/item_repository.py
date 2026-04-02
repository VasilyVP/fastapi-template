from sqlalchemy import or_
from sqlmodel import Session, col, select

from app.models.item import UserItem


class ItemRepository:
    async def list_items(
        self,
        session: Session,
        *,
        owner_username: str,
        query: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[UserItem]:
        statement = select(UserItem).where(UserItem.owner_username == owner_username)

        if query:
            search_term = f"%{query}%"
            statement = statement.where(
                or_(
                    col(UserItem.name).ilike(search_term),
                    col(UserItem.owner_username).ilike(search_term),
                )
            )

        statement = statement.order_by(UserItem.id).offset(skip).limit(limit)
        return list(session.exec(statement).all())

    async def get_item(
        self,
        session: Session,
        *,
        item_id: int,
        owner_username: str,
    ) -> UserItem | None:
        statement = select(UserItem).where(
            UserItem.id == item_id,
            UserItem.owner_username == owner_username,
        )
        return session.exec(statement).first()

    async def create_item(
        self,
        session: Session,
        *,
        owner_username: str,
        name: str,
        price: float,
    ) -> UserItem:
        item = UserItem(name=name, price=price, owner_username=owner_username)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    async def replace_item(
        self,
        session: Session,
        *,
        item: UserItem,
        name: str,
        price: float,
    ) -> UserItem:
        item.name = name
        item.price = price
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    async def patch_item(
        self,
        session: Session,
        *,
        item: UserItem,
        updates: dict[str, str | float],
    ) -> UserItem:
        for field_name, value in updates.items():
            setattr(item, field_name, value)

        session.add(item)
        session.commit()
        session.refresh(item)
        return item


item_repository = ItemRepository()