from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, status_code: int, error_code: str, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(status_code=status_code, detail={"error_code": error_code, "message": message})


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, error_code="UNAUTHORIZED", message=message)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, error_code="FORBIDDEN", message=message)


class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource", error_code: str = "NOT_FOUND"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, error_code=error_code, message=f"{resource} not found")


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, error_code="BAD_REQUEST", message=message)


class ConflictException(AppException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, error_code="CONFLICT", message=message)
