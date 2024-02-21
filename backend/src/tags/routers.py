from fastapi import APIRouter, HTTPException
from typing import List
from src.tags.schemas import TagsRead

import path
import sys


directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent.parent.parent)

from tests.example_responses import tags  # noqa: E402

router = APIRouter(prefix='/api/tags', tags=['tags'])


@router.get('/', response_model=List[TagsRead])
def get_tags():
    return list(tags.values())


@router.get('/{tag_id}/', response_model=TagsRead)
def get_tag(tag_id: int):
    if tag_id not in tags:
        raise HTTPException(status_code=404, detail="Страница не найдена.")
    return tags.get(tag_id)
