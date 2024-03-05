from typing import Annotated, List

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

str150_unique = Annotated[str, mapped_column(String(150), unique=True)]
str150 = Annotated[str, mapped_column(String(150))]
str200 = Annotated[str, mapped_column(String(200))]
user_fk = Annotated[int, mapped_column(ForeignKey("user.id"))]
intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
recipe_id = Annotated[int, mapped_column(ForeignKey("recipe.id"))]


class TagsInRecipe(Base):
    __tablename__ = "tagsinrecipe"
    __table_args__ = (UniqueConstraint("recipe_id", "tag_id"),)

    id: Mapped[intpk] = mapped_column(init=False)
    recipe_id: Mapped[recipe_id]
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"))


class IngredientsInRecipe(Base):
    __tablename__ = "ingredientsinrecipe"
    __table_args__ = (UniqueConstraint("recipe_id", "ingredient_id"),)

    id: Mapped[intpk] = mapped_column(init=False)
    recipe_id: Mapped[recipe_id]
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredient.id"))
    recipe: Mapped["Recipe"] = relationship(
        "Recipe",
        back_populates="ingredients_in_recipe",
    )
    amount: Mapped[int]


"""
class RecipeUserMixin:
    __table_args__ = (UniqueConstraint("recipe_id", "user_id"),)

    id: Mapped[intpk] = mapped_column(init=False)
    recipe_id: Mapped[recipe_id]
    user_id: Mapped[user_fk]


class Cart(RecipeUserMixin, Base):
    __tablename__ = "cart"


class Favorite(RecipeUserMixin, Base):
    __tablename__ = "favorite"
"""


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(255))
    text: Mapped[str]
    # author_id: Mapped[user_fk]
    image: Mapped[str]
    cooking_time: Mapped[int]
    # author: Mapped["User"] = relationship('User', back_populates="recipes")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary="tagsinrecipe",
        back_populates="recipes",
    )
    ingredients_in_recipe: Mapped[List["IngredientsInRecipe"]] = relationship(
        "IngredientsInRecipe",
        back_populates="recipe",
    )
    ingredients: Mapped[List["Ingredient"]] = relationship(
        secondary="ingredientsinrecipe",
        back_populates="recipes",
    )
    # in_favorite: Mapped[List['User']] = relationship(
    #    secondary=lambda: Favorite, back_populates='recipes_in_favorite',
    # )
    # in_cart: Mapped[List['User']] = relationship(
    #    secondary=lambda: Cart, back_populates='recipes_in_cart',
    # )


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str200]
    color: Mapped[str] = mapped_column(String(7))
    slug: Mapped[str] = mapped_column(String(200), unique=True)
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        secondary="tagsinrecipe",
        back_populates="tags",
    )


class Ingredient(Base):
    __tablename__ = "ingredient"

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str200]
    measurement_unit: Mapped[str200]
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        secondary="ingredientsinrecipe",
        back_populates="ingredients",
    )


# class Follow(Base):
#    __tablename__ = 'follow'
#    __table_args__ = (UniqueConstraint('user_id', 'following_id'))

#    id: Mapped[intpk] = mapped_column(init=False)
#    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
#    following_id: Mapped[int] = mapped_column(ForeignKey('user.id'))


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk] = mapped_column(init=False)
    email: Mapped[str150_unique]
    username: Mapped[str150_unique]
    first_name: Mapped[str150]
    last_name: Mapped[str150]
    password: Mapped[str150]


class Token(Base):
    __tablename__ = "token"

    access_token: Mapped[str]
    token_type: Mapped[str] = "bearer"


"""
    recipes: Mapped[List["Recipe"]] = relationship(
        'Recipe', back_populates='author', cascade="all, delete-orphan",
    )
    recipes_in_favorite: Mapped[List['Recipe']] = relationship(
        'Recipe', secondary=lambda: Favorite, back_populates='in_favorite',
    )
    recipes_in_cart: Mapped[List['Recipe']] = relationship(
        'Recipe', secondary=lambda: Cart, back_populates='in_cart',
    )
    # followers: Mapped[List['User']] = relationship(
        secondary=lambda: Follow, back_populates='',
    )
"""
