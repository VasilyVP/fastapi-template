from app.db.mock import fake_users_db
from app.schemas.user import UserInDB


class UserRepository:
    async def get_by_username(self, username: str) -> UserInDB | None:
        return fake_users_db.get(username)


user_repository = UserRepository()
