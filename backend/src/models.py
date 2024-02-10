from database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List, Annotated


str150_unique = Annotated[str, mapped_column(String(150), unique=True, nullable=False)]
str150 = Annotated[str, mapped_column(String(150), nullable=False)]
str200 = Annotated[str, mapped_column(String(200), nullable=False)]
user_fk = Annotated[int, mapped_column(ForeignKey("user.id"), default=None)]
int_not_null = Annotated[int, mapped_column(nullable=False)]
str_not_null = Annotated[str, mapped_column(nullable=False)]
intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class TagsInRecipe(Base):
    __tablename__ = 'tagsinrecipe'

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), primary_key=True)
    recipe: Mapped['Recipe'] = relationship('Recipe', back_populates='tags_in_recipe', default=None)
    tag: Mapped['Tag'] = relationship('Tag', back_populates='tags_in_recipe', default=None)


class IngredientsInRecipe(Base):
    __tablename__ = 'ingredientsinrecipe'

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), primary_key=True)
    recipe: Mapped['Recipe'] = relationship('Recipe', back_populates='ingredients_in_recipe', default=None)
    ingredient: Mapped['Ingredient'] = relationship('Ingredient', back_populates='ingredients_in_recipe', default=None)
    amount: Mapped[int_not_null]


class Recipe(Base):
    __tablename__ = 'recipe'

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str_not_null]
    author_id: Mapped[user_fk]
    image: Mapped[int_not_null]
    cooking_time: Mapped[int_not_null]
    author: Mapped["User"] = relationship('User', back_populates="recipes", default=None)
    tags: Mapped[List["Recipe"]] = relationship(secondary=lambda: TagsInRecipe, back_populates="recipes")
    tags_in_recipe: Mapped[List['TagsInRecipe']] = relationship('TagsInRecipe', back_populates='recipe', default_factory=list)
    ingredients_in_recipe: Mapped[List['IngredientsInRecipe']] = relationship('IngredientsInRecipe', back_populates='recipe', default_factory=list)
    ingredients: Mapped[List['Ingredient']] = relationship(secondary=lambda: IngredientsInRecipe, back_populates='recipes', default_factory=list)


class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str200]
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    recipes: Mapped[List["Recipe"]] = relationship(secondary=lambda: TagsInRecipe, back_populates="tags", default_factory=list)
    tags_in_recipe: Mapped[List['TagsInRecipe']] = relationship('TagsInRecipe', back_populates='tag', default_factory=list)


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str200]
    measurement_unit: Mapped[str200]
    recipes: Mapped[List['Recipe']] = relationship(secondary=lambda: IngredientsInRecipe, back_populates='ingredients', default_factory=list)
    ingredients_in_recipe: Mapped[List['IngredientsInRecipe']] = relationship('IngredientsInRecipe', back_populates='ingredient', default_factory=list)


class Follow(Base):
    __tablename__ = 'follow'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    following_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    # user: Mapped['User'] = relationship('User', back_populates='following', foreign_keys=[user_id])
    # follower: Mapped['User'] = relationship('User', back_populates='follower', foreign_keys=[following_id])


class User(Base):
    __tablename__ = 'user'

    id: Mapped[intpk] = mapped_column(init=False)
    email: Mapped[str150_unique]
    username: Mapped[str150_unique]
    first_name: Mapped[str150]
    last_name: Mapped[str150]
    password: Mapped[str150]
    recipes: Mapped[List["Recipe"]] = relationship('Recipe', back_populates='author', default_factory=list, cascade="all, delete-orphan")
    # followers: Mapped[List['User']] = relationship(secondary=lambda: Follow, back_populates='')

