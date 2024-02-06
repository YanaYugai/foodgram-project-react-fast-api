from database import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    author = relationship('User',  back_populates="recipes")
    image = Column(String, nullable=False)
    cooking_time: int = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True,  nullable=False)
    username = Column(String(150), unique=True,  nullable=False)
    first_name = Column(String(150), unique=True,  nullable=False)
    last_name = Column(String(150), unique=True,  nullable=False)
    password = Column(String(150), unique=True,  nullable=False)
    recipes = relationship('Recipe', back_populates='author')
