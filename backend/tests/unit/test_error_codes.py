from app.core.exceptions import (
    AppException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    BadRequestException,
    ConflictException,
)


def test_unauthorized_maps_to_code():
    exc = UnauthorizedException()
    assert exc.error_code == "UNAUTHORIZED"
    assert exc.status_code == 401


def test_forbidden_maps_to_code():
    exc = ForbiddenException()
    assert exc.error_code == "FORBIDDEN"
    assert exc.status_code == 403


def test_not_found_maps_to_code():
    exc = NotFoundException("Project")
    assert exc.error_code == "NOT_FOUND"
    assert exc.status_code == 404
    assert "Project" in exc.message


def test_bad_request_maps_to_code():
    exc = BadRequestException("Invalid input")
    assert exc.error_code == "BAD_REQUEST"
    assert exc.status_code == 400


def test_conflict_maps_to_code():
    exc = ConflictException("Duplicate")
    assert exc.error_code == "CONFLICT"
    assert exc.status_code == 409


def test_app_exception_detail_format():
    exc = AppException(status_code=422, error_code="VALIDATION_ERROR", message="field required")
    assert exc.detail["error_code"] == "VALIDATION_ERROR"
    assert exc.detail["message"] == "field required"


def test_all_business_exceptions_are_app_exceptions():
    for exc_cls in [UnauthorizedException, ForbiddenException, NotFoundException, BadRequestException, ConflictException]:
        exc = exc_cls()
        assert isinstance(exc, AppException)
