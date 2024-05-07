from pydantic import BaseModel, ConfigDict


class TagsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    color: str
    slug: str
