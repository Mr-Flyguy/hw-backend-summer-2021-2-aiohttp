from __future__ import annotations

from typing import Any, Mapping, Optional

from aiohttp import web


def json_response(
    data: Any,
    *,
    status: int = 200,
    dumps=None,
) -> web.Response:
    # маленький хелпер, чтобы было единообразно
    return web.json_response(data, status=status, dumps=dumps)


def error_json_response(
    *,
    http_status: int,
    status: str,
    message: str = "error",
    data: Optional[Mapping[str, Any]] = None,
) -> web.Response:
    """
    Единый формат ошибок по LMS:
    {
      "status": "...",
      "message": "...",
      "data": {...}
    }
    """
    payload = {
        "status": status,
        "message": message,
        "data": data or {},
    }
    return web.json_response(payload, status=http_status)
