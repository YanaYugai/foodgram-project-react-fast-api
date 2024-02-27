from typing import List

from fastapi import APIRouter, HTTPException

from src.example_responses import tags
from src.tags.schemas import TagsRead

router = APIRouter(prefix='/api/tags', tags=['tags'])


@router.get('/', response_model=List[TagsRead])
def get_tags():
    return list(tags.values())


@router.get('/{tag_id}/', response_model=TagsRead)
def get_tag(tag_id: int):
    if tag_id not in tags:
        raise HTTPException(status_code=404, detail="Страница не найдена.")
    return tags.get(tag_id)
