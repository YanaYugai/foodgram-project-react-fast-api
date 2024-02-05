from pydantic import BaseModel


class TagsRead(BaseModel):
    id: int
    name: str
    color: str
    slug: str
