from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from database import SessionApi
from src.crud.services import delete_token, get_object_by_email_or_error


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
    user = get_object_by_email_or_error(
        session=session,
        email=form_data.email,
        password=form_data.password,
    )
    return {
        "access_token": user.username,
        "token_type": "bearer",
        "auth_token": "string",
    }


@router.delete("/logout/", status_code=204)
def logout(
    session: SessionApi,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    delete_token(session=session, token=token)
