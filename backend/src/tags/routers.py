from typing import List

from fastapi import APIRouter

from backend.database import SessionApi
from backend.src.crud import services
from backend.src.models import Tag
from backend.src.tags.schemas import TagsRead

router = APIRouter(prefix='/api/tags', tags=['tags'])


@router.get('/', response_model=List[TagsRead])
def get_tags(session: SessionApi):
    tags = services.get_objects(session, Tag)
    return tags


@router.get('/{tag_id}/', response_model=TagsRead)
def get_tag(tag_id: int, session: SessionApi):
    tag = services.get_object_by_id_or_error(tag_id, session, Tag)
    return tag
