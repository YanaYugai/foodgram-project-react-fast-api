from pydantic import BaseModel, ConfigDict


class IngredientsInRecipe(BaseModel):
    id: int
    amount: int


class IngredientsRead(BaseModel):
    id: int
    name: str
    measurement_unit: str


class IngredientsFullInRecipeRead(IngredientsRead):
    model_config = ConfigDict(from_attributes=True)
    amount: int
