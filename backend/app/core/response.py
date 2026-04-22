from typing import Any

from fastapi.responses import JSONResponse


def success_response(data: Any = None, message: str = "ok", status_code: int = 200) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"code": 0, "message": message, "data": data})


def error_response(error_code: str, message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"code": -1, "error_code": error_code, "message": message})
