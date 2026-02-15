from __future__ import annotations

import json
from typing import Any, Dict, Optional

from aiohttp import web
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity

from app.web.utils import error_json_response

# Важно: статусы ошибок должны браться из этого словаря (он проверяется тестами).
HTTP_ERROR_CODES: Dict[int, str] = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    409: "conflict",
    500: "internal_server_error",
}


def _parse_http_unprocessable_entity_data(exc: HTTPUnprocessableEntity) -> Dict[str, Any]:
    """
    aiohttp-apispec / webargs кладёт в text JSON-строку с ошибками marshmallow.
    В LMS просят класть эти данные в поле data. :contentReference[oaicite:14]{index=14}
    """
    try:
        if exc.text:
            return json.loads(exc.text)
    except Exception:
        pass
    return {}


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        return await handler(request)

    except HTTPUnprocessableEntity as e:
        # Валидация (marshmallow) -> 400 + data = ошибки валидации
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message="validation_error",
            data=_parse_http_unprocessable_entity_data(e),
        )

    except HTTPException as e:
        http_status = int(getattr(e, "status", 500) or 500)
        status_text = HTTP_ERROR_CODES.get(http_status, HTTP_ERROR_CODES[500])

        # если есть тело (например, мы передадим json-строку), попробуем распарсить в data
        data: Dict[str, Any] = {}
        if getattr(e, "text", None):
            try:
                data = json.loads(e.text)
            except Exception:
                data = {}

        return error_json_response(
            http_status=http_status,
            status=status_text,
            message=getattr(e, "reason", "") or "http_error",
            data=data,
        )

    except Exception:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message="internal_error",
            data={},
        )
