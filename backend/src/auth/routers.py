import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from backend.database import SessionApi
from backend.src.auth.schemas import TokenCreation
from backend.src.auth.utils import create_access_token, oauth2_scheme
from backend.src.crud.services import authenticate_user
from backend.src.models import Token

load_dotenv()


MINUTES = os.getenv('MINUTES')


router = APIRouter(prefix='/api/token', tags=['token'])


@router.post("/login/", response_model=TokenCreation)
def login(
    session: SessionApi,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = authenticate_user(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if MINUTES is None:
        raise ValueError
    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=int(MINUTES),
        )
    ).timestamp()
    expires_delta = timedelta(seconds=expire)
    token = Token(
        access_token=create_access_token(
            subject=user.id,
            expires_delta=expires_delta,
        ),
    )
    session.add(token)
    session.commit()
    return {
        'access_token': token.access_token,
        'token_type': token.token_type,
        'auth_token': token.access_token,
    }


@router.delete("/logout/", status_code=204)
def logout(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    statement = select(Token).where(Token.access_token == token)
    token = session.scalar(statement)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    session.delete(token)
    session.commit()
