from typing import Annotated, Optional

from fastapi import Query
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from backend.src.models import Ingredient, Recipe


class IngredientFilter(Filter):
    name: Optional[str] = None

    class Constants(Filter.Constants):
        model = Ingredient
        search_field_name = "name"
        search_model_fields = ["name"]


class RecipeFilter(Filter):
    author_id: Annotated[
        Optional[int], Field(Query(default=None, alias="author"))
    ]

    class Constants(Filter.Constants):
        model = Recipe
