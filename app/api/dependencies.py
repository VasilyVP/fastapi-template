from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core.security import decode_token
from app.repositories.user_repository import user_repository
from app.schemas.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")


def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = decode_token(token)
        username_raw = payload.get("sub")
    except InvalidTokenError as exc:
        raise credentials_exception() from exc

    if not isinstance(username_raw, str) or not username_raw:
        raise credentials_exception()

    user = await user_repository.get_by_username(username_raw)
    if user is None:
        raise credentials_exception()

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
ActiveUserDep = Annotated[User, Depends(get_current_active_user)]
