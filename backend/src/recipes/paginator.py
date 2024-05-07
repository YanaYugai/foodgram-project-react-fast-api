from __future__ import annotations

import math
from typing import Generic, Optional, Sequence, TypeVar

from fastapi import Query
from fastapi_paginate.bases import AbstractPage, AbstractParams, RawParams
from pydantic import BaseModel
from starlette.requests import Request

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    limit: int = Query(6, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.limit,
            offset=self.limit * (self.page - 1),
        )


class Page(AbstractPage[T], Generic[T]):
    next: Optional[str] = None
    previous: Optional[str] = None
    count: Optional[int] = 0
    results: Sequence[T]

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
        request: Request,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        next = None
        previous = None

        last_page = math.ceil(total / params.limit)
        prev_page = params.page - 1

        query_params = str(request.query_params)
        previous = (
            f"""{request.url.path}?{query_params.replace(
                f'page={params.page}',
                f'page={prev_page}',
            )}"""
            if prev_page >= 1
            else None
        )
        next = (
            f"""{request.url.path}?{query_params.replace(
                f'page={params.page}',
                f'page={params.page + 1}',
            )}"""
            if params.page + 1 <= last_page
            else None
        )
        return cls(
            count=total,
            results=items,
            next=next,
            previous=previous,
        )
