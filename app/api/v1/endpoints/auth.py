from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import Settings, get_settings
from app.schemas.user import Token
from app.services.auth_service import auth_service


router = APIRouter(prefix="", tags=["auth"])


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
) -> Token:
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    access_token = auth_service.issue_access_token(
        username=user.username,
        expires_minutes=settings.access_token_expire_minutes,
    )
    return Token(access_token=access_token, token_type="bearer")
