from pydantic import BaseModel


class TokenCreation(BaseModel):
    auth_token: str
    access_token: str
    token_type: str
