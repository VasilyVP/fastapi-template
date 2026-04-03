from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.security import (
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    get_password_hash,
)
from app.models.user import User
from app.services.auth_service import AuthService


def make_user(
    username: str = "testuser",
    password: str = "secret",
    disabled: bool = False,
) -> User:
    return User(
        username=username,
        hashed_password=get_password_hash(password),
        email="test@example.com",
        full_name="Test User",
        disabled=disabled,
    )


@pytest.fixture
def service() -> AuthService:
    return AuthService()


# ---------------------------------------------------------------------------
# authenticate_user
# ---------------------------------------------------------------------------


async def test_authenticate_user_returns_user_on_valid_credentials(service: AuthService) -> None:
    user = make_user()
    session = MagicMock()
    with patch(
        "app.services.auth_service.user_repository.get_by_username",
        new=AsyncMock(return_value=user),
    ):
        result = await service.authenticate_user("testuser", "secret", session)
    assert result is user


async def test_authenticate_user_returns_none_when_user_not_found(service: AuthService) -> None:
    session = MagicMock()
    with patch(
        "app.services.auth_service.user_repository.get_by_username",
        new=AsyncMock(return_value=None),
    ):
        result = await service.authenticate_user("unknown", "secret", session)
    assert result is None


async def test_authenticate_user_returns_none_on_wrong_password(service: AuthService) -> None:
    user = make_user()
    session = MagicMock()
    with patch(
        "app.services.auth_service.user_repository.get_by_username",
        new=AsyncMock(return_value=user),
    ):
        result = await service.authenticate_user("testuser", "wrongpassword", session)
    assert result is None


async def test_authenticate_user_calls_verify_password_when_user_not_found(
    service: AuthService,
) -> None:
    """Timing attack mitigation: verify_password must be called even for unknown users."""
    session = MagicMock()
    with patch(
        "app.services.auth_service.user_repository.get_by_username",
        new=AsyncMock(return_value=None),
    ):
        with patch("app.services.auth_service.verify_password", return_value=False) as mock_verify:
            await service.authenticate_user("unknown", "anypassword", session)
    mock_verify.assert_called_once()


# ---------------------------------------------------------------------------
# issue_access_token
# ---------------------------------------------------------------------------


def test_issue_access_token_contains_expected_claims(service: AuthService) -> None:
    user = make_user()
    token = service.issue_access_token(user, expires_minutes=15)
    payload = decode_access_token(token)
    assert payload["sub"] == user.username
    assert payload["email"] == user.email
    assert payload["full_name"] == user.full_name


def test_issue_access_token_returns_non_empty_string(service: AuthService) -> None:
    token = service.issue_access_token(make_user(), expires_minutes=15)
    assert isinstance(token, str) and token


# ---------------------------------------------------------------------------
# issue_refresh_token
# ---------------------------------------------------------------------------


def test_issue_refresh_token_contains_expected_claims(service: AuthService) -> None:
    user = make_user()
    token = service.issue_refresh_token(user, expires_days=7)
    payload = decode_refresh_token(token)
    assert payload["sub"] == user.username
    assert payload["email"] == user.email
    assert payload["full_name"] == user.full_name


def test_issue_refresh_token_returns_non_empty_string(service: AuthService) -> None:
    token = service.issue_refresh_token(make_user(), expires_days=7)
    assert isinstance(token, str) and token


# ---------------------------------------------------------------------------
# issue_token_pair
# ---------------------------------------------------------------------------


def test_issue_token_pair_returns_valid_access_and_refresh_tokens(service: AuthService) -> None:
    user = make_user()
    access_token, refresh_token = service.issue_token_pair(
        user, access_expires_minutes=15, refresh_expires_days=7
    )
    assert decode_access_token(access_token)["sub"] == user.username
    assert decode_refresh_token(refresh_token)["sub"] == user.username


def test_issue_token_pair_access_and_refresh_are_distinct(service: AuthService) -> None:
    user = make_user()
    access_token, refresh_token = service.issue_token_pair(
        user, access_expires_minutes=15, refresh_expires_days=7
    )
    assert access_token != refresh_token


# ---------------------------------------------------------------------------
# refresh_access_token
# ---------------------------------------------------------------------------


async def test_refresh_access_token_returns_new_access_token_on_success(
    service: AuthService,
) -> None:
    user = make_user()
    refresh_token = create_refresh_token(
        data={"sub": user.username, "email": user.email, "full_name": user.full_name},
        expires_delta=timedelta(days=7),
    )
    session = MagicMock()
    with patch(
        "app.services.auth_service.user_repository.get_by_username",
        new=AsyncMock(return_value=user),
    ):
        result = await service.refresh_access_token(refresh_token, expires_minutes=15, session=session)
    assert result is not None
    assert decode_access_token(result)["sub"] == user.username


async def test_refresh_access_token_returns_none_on_invalid_token(service: AuthService) -> None:
    session = MagicMock()
    result = await service.refresh_access_token(
        "not.a.valid.token", expires_minutes=15, session=session
    )
    assert result is None


async def test_refresh_access_token_returns_none_when_user_not_found(
    service: AuthService,
) -> None:
    user = make_user()
    refresh_token = create_refresh_token(
        data={"sub": user.username, "email": user.email, "full_name": user.full_name},
        expires_delta=timedelta(days=7),
    )
    session = MagicMock()
    with patch(
        "app.services.auth_service.user_repository.get_by_username",
        new=AsyncMock(return_value=None),
    ):
        result = await service.refresh_access_token(refresh_token, expires_minutes=15, session=session)
    assert result is None


async def test_refresh_access_token_returns_none_when_user_is_disabled(
    service: AuthService,
) -> None:
    user = make_user(disabled=True)
    refresh_token = create_refresh_token(
        data={"sub": user.username, "email": user.email, "full_name": user.full_name},
        expires_delta=timedelta(days=7),
    )
    session = MagicMock()
    with patch(
        "app.services.auth_service.user_repository.get_by_username",
        new=AsyncMock(return_value=user),
    ):
        result = await service.refresh_access_token(refresh_token, expires_minutes=15, session=session)
    assert result is None


async def test_refresh_access_token_returns_none_when_sub_claim_is_missing(
    service: AuthService,
) -> None:
    refresh_token = create_refresh_token(
        data={"email": "test@example.com"},
        expires_delta=timedelta(days=7),
    )
    session = MagicMock()
    result = await service.refresh_access_token(refresh_token, expires_minutes=15, session=session)
    assert result is None
