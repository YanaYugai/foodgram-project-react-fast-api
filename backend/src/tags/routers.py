from typing import List, Sequence

from fastapi import APIRouter

from database import SessionApi
from src.crud import services
from src.models import Tag

from .schemas import TagsRead

router = APIRouter(prefix='/api/tags', tags=['tags'])


@router.get('/', response_model=List[TagsRead])
def get_tags(session: SessionApi) -> Sequence[Tag]:
    tags = services.get_objects(session, Tag)
    return tags


@router.get('/{tag_id}/', response_model=TagsRead)
def get_tag(tag_id: int, session: SessionApi) -> Tag:
    tag = services.get_object_by_id_or_error(tag_id, session, Tag)
    return tag
