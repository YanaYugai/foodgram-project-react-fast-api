from pydantic import BaseModel, Field
from typing import List
from backend.src.ingredients.schemas import (
    IngredientsFullInRecipeRead,
    IngredientsInRecipe,
)
from backend.src.users.schemas import AuthorRead
from backend.src.tags.schemas import TagsRead


class RecipeReadShort(BaseModel):
    id: int
    name: str = Field(max_length=200)
    image: str
    cooking_time: int = Field(ge=1)


class RecipeCreate(BaseModel):
    ingredients: List['IngredientsInRecipe']
    tags: List[int]
    image: str
    text: str
    cooking_time: int = Field(ge=1)
    name: str = Field(max_length=200)


class RecipeRead(RecipeReadShort):
    tags: List['TagsRead']
    author: AuthorRead
    ingredients: List['IngredientsFullInRecipeRead']
    is_favorited: bool
    is_in_shopping_cart: bool
    text: str
