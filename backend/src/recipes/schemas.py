from pydantic import BaseModel, Field, EmailStr
from typing import List


class TagsRead(BaseModel):
    id: int
    name: str
    color: str
    slug: str


class IngredientsRead(BaseModel):
    id: int
    name: str
    measurement_unit: str
    amount: int


class IngredientsInRecipe(BaseModel):
    id: int
    amount: int


class AuthorRead(BaseModel):
    email: EmailStr
    id: int
    username: str
    first_name: str
    last_name: str
    is_subscribed: bool


class RecipeCreate(BaseModel):
    ingredients: List['IngredientsInRecipe']
    tags: List[int]
    image: str
    text: str
    cooking_time: int = Field(ge=1)
    name: str = Field(max_length=200)


class RecipeRead(BaseModel):
    id: int
    tags: List['TagsRead']
    author: AuthorRead
    ingredients: List['IngredientsRead']
    is_favorited: bool
    is_in_shopping_cart: bool
    name: str = Field(max_length=200)
    image: str
    text: str
    cooking_time: int = Field(ge=1)
