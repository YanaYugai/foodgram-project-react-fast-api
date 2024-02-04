from pydantic import BaseModel, Field, EmailStr

class IngredientsRead(BaseModel):
    id: int
    name: str
    measurement_unit: str
