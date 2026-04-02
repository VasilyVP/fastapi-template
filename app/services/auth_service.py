from datetime import timedelta

from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.core.security import (
    DUMMY_HASH,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import user_repository


class AuthService:
    async def authenticate_user(self, username: str, password: str, session: Session) -> User | None:
        user = await user_repository.get_by_username(username, session)
        if user is None:
            # Keep timing similar to real checks to reduce user enumeration signals.
            verify_password(password, DUMMY_HASH)
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def issue_access_token(self, user: User, expires_minutes: int) -> str:
        return create_access_token(
            data={
                "sub": user.username,
                "email": user.email,
                "full_name": user.full_name,
            },
            expires_delta=timedelta(minutes=expires_minutes),
        )

    def issue_refresh_token(self, user: User, expires_days: int) -> str:
        return create_refresh_token(
            data={
                "sub": user.username,
                "email": user.email,
                "full_name": user.full_name,
            },
            expires_delta=timedelta(days=expires_days),
        )

    def issue_token_pair(
        self,
        user: User,
        access_expires_minutes: int,
        refresh_expires_days: int,
    ) -> tuple[str, str]:
        access_token = self.issue_access_token(user, access_expires_minutes)
        refresh_token = self.issue_refresh_token(user, refresh_expires_days)
        return access_token, refresh_token

    async def refresh_access_token(
        self,
        refresh_token: str,
        expires_minutes: int,
        session: Session,
    ) -> str | None:
        try:
            payload = decode_refresh_token(refresh_token)
        except InvalidTokenError:
            return None

        username_raw = payload.get("sub")
        if not isinstance(username_raw, str) or not username_raw:
            return None

        user = await user_repository.get_by_username(username_raw, session)
        if user is None or user.disabled:
            return None

        return self.issue_access_token(user, expires_minutes)


auth_service = AuthService()
