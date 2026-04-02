from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.db.session import get_session
from app.core.security import decode_access_token
from app.schemas.user import UserRead


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")
SessionDep = Annotated[Session, Depends(get_session)]


def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserRead:
    try:
        payload = decode_access_token(token)
        username_raw = payload.get("sub")
        email_raw = payload.get("email")
        full_name_raw = payload.get("full_name")
    except InvalidTokenError as exc:
        raise credentials_exception() from exc

    if not isinstance(username_raw, str) or not username_raw:
        raise credentials_exception()

    email = email_raw if isinstance(email_raw, str) else None
    full_name = full_name_raw if isinstance(full_name_raw, str) else None

    return UserRead(
        username=username_raw,
        email=email,
        full_name=full_name,
    )
