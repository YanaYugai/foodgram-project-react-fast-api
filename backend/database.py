from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Session,
    sessionmaker,
)

from backend.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    with LocalSession() as session:
        yield session


SessionApi = Annotated[Session, Depends(get_db)]


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""
