from pydantic import BaseModel, ConfigDict, EmailStr


class TokenCreation(BaseModel):
    auth_token: str
    access_token: str
    token_type: str


class UserTokenCreation(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)
