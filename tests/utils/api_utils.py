import json
from pathlib import Path
from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse

BASE_URL = "https://serverest.dev"
JSON_HEADERS = {"Content-Type": "application/json"}
RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"


def post_json(
    request: APIRequestContext,
    endpoint: str,
    payload: dict[str, Any] | str,
    headers: dict[str, str] | None = None,
) -> APIResponse:
    request_headers = dict(JSON_HEADERS)
    if headers:
        request_headers.update(headers)

    data = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    return request.post(endpoint, headers=request_headers, data=data)


def put_json(
    request: APIRequestContext,
    endpoint: str,
    payload: dict[str, Any] | str,
    headers: dict[str, str] | None = None,
) -> APIResponse:
    request_headers = dict(JSON_HEADERS)
    if headers:
        request_headers.update(headers)

    data = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    return request.put(endpoint, headers=request_headers, data=data)


def parse_response_body(response: APIResponse) -> dict[str, Any]:
    return response.json()


def load_json_resource(relative_path: str) -> dict[str, Any]:
    file_path = RESOURCES_DIR / relative_path
    if not file_path.exists():
        raise FileNotFoundError(f"Resource not found: {file_path}")
    with file_path.open("r", encoding="utf-8") as resource_file:
        return json.load(resource_file)
