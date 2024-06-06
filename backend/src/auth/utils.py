from datetime import datetime, timedelta
from typing import Any, Optional, Union

from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from passlib.context import CryptContext
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from config import SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


class OAuth2PasswordToken(OAuth2PasswordBearer):
    """
    Авторизация по протоколу OAuth2. Используется bearer token.

    Вместо названия схемы "Bearer" используется "Token".
    """

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


class OAuth2PasswordToken_not_necessary(OAuth2PasswordBearer):
    """
    Авторизация по протоколу OAuth2. Используется bearer token.

    Вместо названия схемы "Bearer" используется "Token".

    Используется вместо OAuth2PasswordToken, в тех случаях,
    где пользователь может быть не авторизован.
    """

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization:
            return None
        if scheme.lower() != "token":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"Authorization": "Token"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordToken(tokenUrl="api/auth/token/login/")
oauth2_scheme_token_not_necessary = OAuth2PasswordToken_not_necessary(
    tokenUrl="api/auth/token/login/",
)


def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta,
) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
