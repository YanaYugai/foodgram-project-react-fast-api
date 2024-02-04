import pydantic
from pydantic import EmailStr


class UserCreate(pydantic.BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str


class UserResult(pydantic.BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
