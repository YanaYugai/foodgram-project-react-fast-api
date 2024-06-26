from typing import List

from pydantic import BaseModel, ConfigDict, Field

from src.ingredients.schemas import (
    IngredientsFullInRecipeRead,
    IngredientsInRecipe,
)
from src.tags.schemas import TagsRead
from src.users.schemas import AuthorRead, RecipeReadShort


class RecipeCreate(BaseModel):
    ingredients: List['IngredientsInRecipe']
    tags: List[int]
    image: str
    text: str
    cooking_time: int = Field(ge=1)
    name: str = Field(max_length=200)


class RecipeRead(RecipeReadShort):
    model_config = ConfigDict(from_attributes=True)
    tags: list['TagsRead']
    author: AuthorRead
    ingredients: list['IngredientsFullInRecipeRead']
    is_favorited: bool
    is_in_shopping_cart: bool
    text: str
