from database import Base
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List, Annotated


str150_unique = Annotated[str, mapped_column(String(150), unique=True, nullable=False)]
str150 = Annotated[str, mapped_column(String(150), nullable=False)]
str200 = Annotated[str, mapped_column(String(200), nullable=False)]
user_fk = Annotated[int, mapped_column(ForeignKey("user.id"))]
int_not_null = Annotated[int, mapped_column(nullable=False)]
str_not_null = Annotated[str, mapped_column(nullable=False)]


class User(Base):
    __tablename__ = 'user'

    email: Mapped[str150_unique]
    username: Mapped[str150_unique]
    first_name: Mapped[str150]
    last_name: Mapped[str150]
    password: Mapped[str150]
    recipes: Mapped[List["Recipe"]] = relationship('Recipe', back_populates='author', default_factory=list, cascade="all, delete-orphan")


TagsInRecipe = Table(
    "tagsinrecipe",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipe.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Recipe(Base):
    __tablename__ = 'recipe'

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str_not_null]
    author_id: Mapped[user_fk]
    image: Mapped[int_not_null]
    cooking_time: Mapped[int_not_null]
    author: Mapped["User"] = relationship('User', back_populates="recipes", default=None)
    tags: Mapped[List["Recipe"]] = relationship(secondary=lambda: TagsInRecipe, back_populates="recipes_tags", default_factory=list)


class Tag(Base):
    __tablename__ = 'tag'

    name: Mapped[str200]
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    recipes: Mapped[List["Recipe"]] = relationship(secondary=lambda: TagsInRecipe, back_populates="tags", default_factory=list)


class Ingredient(Base):
    __tablename__ = 'ingredient'

    name: Mapped[str200]
    measurement_unit: Mapped[str200]






