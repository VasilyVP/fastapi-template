from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SessionDep, credentials_exception, oauth2_scheme
from app.core.config import Settings, get_settings
from app.schemas.user import AccessToken, TokenPair
from app.services.auth_service import auth_service


router = APIRouter(prefix="", tags=["auth"])


@router.post("/token", response_model=TokenPair)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
    session: SessionDep,
) -> TokenPair:
    user = await auth_service.authenticate_user(form_data.username, form_data.password, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    access_token, refresh_token = auth_service.issue_token_pair(
        user,
        access_expires_minutes=settings.access_token_expire_minutes,
        refresh_expires_days=settings.refresh_token_expire_days,
    )
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=AccessToken)
async def refresh_access_token(
    refresh_token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
    session: SessionDep,
) -> AccessToken:
    access_token = await auth_service.refresh_access_token(
        refresh_token=refresh_token,
        expires_minutes=settings.access_token_expire_minutes,
        session=session,
    )
    if access_token is None:
        raise credentials_exception()

    return AccessToken(access_token=access_token)
