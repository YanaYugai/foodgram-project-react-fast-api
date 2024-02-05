from pydantic import BaseModel, EmailStr


class UserResponseCreation(BaseModel):
    email: EmailStr
    id: int
    username: str
    first_name: str
    last_name: str


class AuthorRead(UserResponseCreation):
    is_subscribed: bool


class UserCreation(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str
