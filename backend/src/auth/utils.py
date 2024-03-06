from crud.services import get_object_by_email_or_error
from passlib.context import CryptContext

from database import SessionApi

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(session: SessionApi, email: str, password: str):
    user = get_object_by_email_or_error(session=session, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
