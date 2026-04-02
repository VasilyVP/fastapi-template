from sqlalchemy import or_
from sqlmodel import Session, col, select

from app.models.user import User


class UserRepository:
    async def get_by_username(self, username: str, session: Session) -> User | None:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

    async def list_users(
        self,
        session: Session,
        *,
        query: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        statement = select(User)

        if query:
            search_term = f"%{query}%"
            statement = statement.where(
                or_(
                    col(User.username).ilike(search_term),
                    col(User.email).ilike(search_term),
                    col(User.full_name).ilike(search_term),
                )
            )

        statement = statement.order_by(User.username).offset(skip).limit(limit)
        return list(session.exec(statement).all())


user_repository = UserRepository()
