import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from auth.utils import create_access_token
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from models import Token
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from database import SessionApi
from src.crud.services import authenticate_user, delete_token

load_dotenv()


MINUTES = os.getenv('MINUTES')


class OAuth2PasswordToken(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "token":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"Authorization": "Token"},
                )
            else:
                return None
        return param


router = APIRouter(prefix='/api/token', tags=['token'])

oauth2_scheme = OAuth2PasswordToken(tokenUrl="api/token/login/")


@router.post("/login/")
def login(
    session: SessionApi,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = authenticate_user(
        session=session,
        email=form_data.email,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if MINUTES is None:
        raise ValueError
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(MINUTES))
    token = Token(
        access_token=create_access_token(
            subject=user.id,
            expires_delta=expire,
        ),
    )
    return token


@router.delete("/logout/", status_code=204)
def logout(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    delete_token(session=session, token=token)
