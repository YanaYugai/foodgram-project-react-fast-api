import pydantic


class User(pydantic.BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
