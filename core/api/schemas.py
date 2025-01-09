from typing import TypeVar, Any, Generic

from pydantic import Field

from ninja import Schema

from core.api.filters import PaginationOut

TData = TypeVar('TData')
TListItem = TypeVar('TListItem')
TDetailItem = TypeVar('TDetailItem')


class PingResponseSchema(Schema):
    result: bool


class ListPaginatedResponse(Schema, Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOut


class DetailResponse(Schema, Generic[TDetailItem]):
    item: TDetailItem


class ApiResponse(Schema, Generic[TData]):
    data: TData | dict = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)
