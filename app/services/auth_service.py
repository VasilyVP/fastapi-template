from datetime import timedelta

from app.core.security import DUMMY_HASH, create_access_token, verify_password
from app.repositories.user_repository import user_repository
from app.schemas.user import UserInDB


class AuthService:
    async def authenticate_user(self, username: str, password: str) -> UserInDB | None:
        user = await user_repository.get_by_username(username)
        if user is None:
            # Keep timing similar to real checks to reduce user enumeration signals.
            verify_password(password, DUMMY_HASH)
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def issue_access_token(self, username: str, expires_minutes: int) -> str:
        return create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=expires_minutes),
        )


auth_service = AuthService()
