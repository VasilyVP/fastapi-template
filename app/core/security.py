from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import get_settings


password_hash = PasswordHash.recommended()
settings = get_settings()
DUMMY_HASH = password_hash.hash("dummypassword")
TOKEN_TYPE_CLAIM = "token_type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def _create_token(
    data: dict[str, Any],
    token_type: str,
    expires_delta: timedelta,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, TOKEN_TYPE_CLAIM: token_type})
    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    return _create_token(
        data=data,
        token_type=ACCESS_TOKEN_TYPE,
        expires_delta=expires_delta or timedelta(minutes=15),
    )


def create_refresh_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    return _create_token(
        data=data,
        token_type=REFRESH_TOKEN_TYPE,
        expires_delta=expires_delta,
    )


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(  # pyright: ignore[reportUnknownMemberType]
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except InvalidTokenError as exc:
        raise InvalidTokenError("Could not validate credentials") from exc

    return payload


def _decode_token_by_type(token: str, expected_token_type: str) -> dict[str, Any]:
    payload = decode_token(token)
    token_type = payload.get(TOKEN_TYPE_CLAIM)
    if token_type != expected_token_type:
        raise InvalidTokenError("Invalid token type")
    return payload


def decode_access_token(token: str) -> dict[str, Any]:
    return _decode_token_by_type(token, ACCESS_TOKEN_TYPE)


def decode_refresh_token(token: str) -> dict[str, Any]:
    return _decode_token_by_type(token, REFRESH_TOKEN_TYPE)
