from app.schemas.common import ApiResponse, PaginatedResponse


def test_api_response_serializable():
    resp = ApiResponse(code=0, message="ok", data={"key": "value"})
    dumped = resp.model_dump()
    assert dumped["code"] == 0
    assert dumped["message"] == "ok"
    assert dumped["data"] == {"key": "value"}


def test_api_response_defaults():
    resp = ApiResponse()
    assert resp.code == 0
    assert resp.message == "ok"
    assert resp.data is None


def test_paginated_response_fields():
    resp = PaginatedResponse(total=100, page=2, page_size=20, items=[{"id": 1}])
    dumped = resp.model_dump()
    assert dumped["total"] == 100
    assert dumped["page"] == 2
    assert dumped["page_size"] == 20
    assert len(dumped["items"]) == 1


def test_paginated_response_defaults():
    resp = PaginatedResponse()
    assert resp.total == 0
    assert resp.page == 1
    assert resp.page_size == 20
    assert resp.items == []


def test_error_response_data_null():
    resp = ApiResponse(code=-1, message="error", data=None)
    dumped = resp.model_dump()
    assert dumped["code"] == -1
    assert dumped["data"] is None
