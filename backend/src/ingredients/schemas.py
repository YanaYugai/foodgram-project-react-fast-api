from pydantic import BaseModel


class IngredientsRead(BaseModel):
    id: int
    name: str
    measurement_unit: str


class IngredientsFullInRecipeRead(IngredientsRead):
    amount: int
