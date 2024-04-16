from typing import Annotated, List

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base  # type: ignore

str150_unique = Annotated[str, mapped_column(String(150), unique=True)]
str150 = Annotated[str, mapped_column(String(150))]
str200 = Annotated[str, mapped_column(String(200))]
user_fk = Annotated[int, mapped_column(ForeignKey("user.id"))]
intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
recipe_id = Annotated[int, mapped_column(ForeignKey("recipe.id"))]


class TagsInRecipe(Base):
    __tablename__ = "tagsinrecipe"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), primary_key=True)
    # tag: Mapped['Tag'] = relationship(
    #    'Tag', back_populates='taginrecipe', init=False
    # )


class IngredientsInRecipe(Base):
    __tablename__ = "ingredientsinrecipe"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id"), primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient.id"),
        primary_key=True,
        confirm_deleted_rows=False,
    )
    amount: Mapped[int]
    # recipe: Mapped["Recipe"] = relationship(
    #    "Recipe",
    #    back_populates="ingredients",
    #    init=False,
    # )
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient",
        # back_populates="ingredients_in_recipe",
        init=False,
    )
    id: AssociationProxy[int] = association_proxy(
        "ingredient", "id", init=False
    )
    name: AssociationProxy[str200] = association_proxy(
        "ingredient", "name", init=False
    )
    measurement_unit: AssociationProxy[str200] = association_proxy(
        "ingredient", "measurement_unit", init=False
    )


"""

class RecipeUserMixin:

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id"), primary_key=True
    )
    user_id: Mapped[user_fk] = mapped_column(
        ForeignKey("int"), primary_key=True
    )


class Cart(RecipeUserMixin, Base):
    __tablename__ = "cart"


class Favorite(RecipeUserMixin, Base):
    __tablename__ = "favorite"
"""


class Ingredient(Base):
    __tablename__ = "ingredient"

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str200]
    measurement_unit: Mapped[str200]
    """
    ingredients_in_recipe: Mapped[List["IngredientsInRecipe"]] = relationship(
        "IngredientsInRecipe",
        back_populates="ingredient",
        init=False,
    )
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        secondary="ingredientsinrecipe",
        back_populates="ingredients_in_recipe",
        init=False,
    )
    """


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(255))
    text: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    image: Mapped[str]
    cooking_time: Mapped[int]
    author: Mapped["User"] = relationship(
        'User',
        back_populates="recipes",
        init=False,
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary="tagsinrecipe",
        # back_populates="recipes",
        init=False,
    )
    ingredients: Mapped[List["IngredientsInRecipe"]] = relationship(
        "IngredientsInRecipe",
        # back_populates="recipe",
        init=False,
        cascade="all, delete",
    )
    """
    ingredients_in_recipe: Mapped[List["Ingredient"]] = relationship(
        secondary="ingredientsinrecipe",
        back_populates="recipes",
        init=False,
    )
    # in_favorite: Mapped[List['User']] = relationship(
    #    secondary=lambda: Favorite, back_populates='recipes_in_favorite',
    # )
    # in_cart: Mapped[List['User']] = relationship(
    #    secondary=lambda: Cart, back_populates='recipes_in_cart',
    # )
"""


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str200]
    color: Mapped[str] = mapped_column(String(7))
    slug: Mapped[str] = mapped_column(String(200), unique=True)
    """
    taginrecipe: Mapped[List["TagsInRecipe"]] = relationship(
        'TagsInRecipe', back_populates='tag', init=False
    )
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        secondary="tagsinrecipe",
        back_populates="tags",
        init=False,
    )
"""


class Follow(Base):
    __tablename__ = 'follow'
    __table_args__ = (UniqueConstraint('user_id', 'following_id'),)

    id: Mapped[intpk] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    following_id: Mapped[int] = mapped_column(ForeignKey('user.id'))


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk] = mapped_column(init=False)
    email: Mapped[str150_unique]
    username: Mapped[str150_unique]
    first_name: Mapped[str150]
    last_name: Mapped[str150]
    password: Mapped[str150]
    followers: Mapped[List['User']] = relationship(
        "User",
        secondary="follow",
        primaryjoin=Follow.following_id == id,
        secondaryjoin=Follow.user_id == id,
        backref="following",
        init=False,
    )
    recipes: Mapped[List["Recipe"]] = relationship(
        'Recipe',
        back_populates='author',
        cascade="all, delete-orphan",
        init=False,
    )


class Token(Base):
    __tablename__ = "token"

    id: Mapped[intpk] = mapped_column(init=False)
    access_token: Mapped[str]
    token_type: Mapped[str] = mapped_column(default="bearer")


"""
    recipes_in_favorite: Mapped[List['Recipe']] = relationship(
        'Recipe', secondary=lambda: Favorite, back_populates='in_favorite',
    )
    recipes_in_cart: Mapped[List['Recipe']] = relationship(
        'Recipe', secondary=lambda: Cart, back_populates='in_cart',
    )
    )
"""
