"""Ошибки HTTP и чтения ответа MindVoice."""

from __future__ import annotations

import httpx
from pydantic import JsonValue, ValidationError

from .models import ErrorResponse, FieldViolation


class HTTPError(Exception):
    """Ответ MindVoice с HTTP-статусом вне диапазона 2xx."""

    def __init__(self, response: httpx.Response, body: bytes) -> None:
        """Сохраняет статус, служебные заголовки и сведения из JSON-ошибки API."""
        self.status_code = response.status_code
        self.retry_after = response.headers.get("Retry-After")
        self.content_range = response.headers.get("Content-Range")
        self.request_id = response.headers.get("X-Request-ID")
        self.code: str | None = None
        self.message: str | None = None
        self.violations: list[FieldViolation] = []
        self.details: dict[str, JsonValue] | None = None

        # Ответ прокси или ответ без тела сохраняет HTTP-статус и заголовки.
        if body:
            try:
                error = ErrorResponse.model_validate_json(body, extra="ignore").error
            except ValidationError:
                pass
            else:
                self.code = error.code
                self.message = error.message
                self.violations = error.violations
                self.details = error.details
                self.request_id = error.request_id or self.request_id

        suffix = f" ({self.code})" if self.code else ""
        super().__init__(f"MindVoice: HTTP {self.status_code}{suffix}")


class ResponseError(Exception):
    """Успешный HTTP-ответ с телом, которое не соответствует схеме операции."""

    def __init__(self, response: httpx.Response) -> None:
        """Сохраняет статус и ID запроса без содержимого ответа."""
        self.status_code = response.status_code
        self.request_id = response.headers.get("X-Request-ID")
        super().__init__(f"MindVoice: некорректный JSON-ответ (HTTP {self.status_code})")
