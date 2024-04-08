from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str


class UserResponseCreation(UserBase):
    id: int


class AuthorRead(UserResponseCreation):
    is_subscribed: bool

    model_config = ConfigDict(from_attributes=True)


class UserCreation(UserBase):
    password: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("username")
    def validate_bad_words(cls, username: str):
        if username == "me":
            raise ValueError("bad username, choose another")
        return username


class UserTokenCreation(BaseModel):
    email: EmailStr
    password: str


class UserPasswordReset(BaseModel):
    new_password: str
    current_password: str

    model_config = ConfigDict(from_attributes=True)
