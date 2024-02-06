from pydantic import BaseModel, EmailStr, validator


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

    @validator("username")  # pydantic v1
    def validate_bad_words(cls, username: str):
        if username == "me":
            raise ValueError("bad username, choose another")
        return username
