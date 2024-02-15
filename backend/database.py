from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedAsDataclass
from config import DB_HOST, DB_NAME, DB_PASS, DB_USER
from typing import Annotated, Generator
from sqlalchemy.orm import Session
from fastapi import Depends


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
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
