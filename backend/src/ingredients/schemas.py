from pydantic import BaseModel


class IngredientsInRecipe(BaseModel):
    id: int
    amount: int


class IngredientsRead(BaseModel):
    id: int
    name: str
    measurement_unit: str


class IngredientsFullInRecipeRead(IngredientsRead):
    amount: int
