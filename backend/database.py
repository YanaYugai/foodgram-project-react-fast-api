from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedAsDataclass
from config import DB_HOST, DB_NAME, DB_PASS, DB_USER
from typing import Annotated
from sqlalchemy.orm import mapped_column, Mapped

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""
    id: Mapped[intpk] = mapped_column(init=False)
