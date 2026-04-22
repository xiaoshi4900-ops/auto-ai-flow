from pydantic import BaseModel
from typing import Any


class PaginationRequest(BaseModel):
    page: int = 1
    page_size: int = 20


class PaginatedResponse(BaseModel):
    total: int = 0
    page: int = 1
    page_size: int = 20
    items: list[Any] = []


class ApiResponse(BaseModel):
    code: int = 0
    message: str = "ok"
    data: Any = None
