"""Общие правила HTTP-запросов и потоковой передачи файлов MindVoice."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator, Mapping, Sequence
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from types import TracebackType
from typing import BinaryIO, Self, TypedDict, TypeVar, Unpack, cast
from urllib.parse import quote
from uuid import UUID

import httpx
from anyio import CancelScope, to_thread
from pydantic import BaseModel, JsonValue, ValidationError

from ._errors import HTTPError, ResponseError

DEFAULT_BASE_URL = "https://api.mindvoice.pro"
_MAX_ERROR_BYTES = 64 * 1024
_Response = TypeVar("_Response", bound=BaseModel)
_PathValue = str | int | UUID
_QueryScalar = str | int | float | bool | UUID
_QueryValue = _QueryScalar | Sequence[_QueryScalar] | None


@dataclass(frozen=True)
class _Upload:
    """Данные одной записи для загрузки через multipart."""

    file: BinaryIO
    filename: str
    content_type: str
    metadata: Mapping[str, JsonValue] | None
    recorded_at: datetime | str | None
    retention_days: int | None
    check_duplicates: bool | None

    def fields(self) -> dict[str, str | int | bool]:
        """Подготавливает поля multipart, передавая явно заданные значения."""
        if not self.filename.strip() or any(char in self.filename for char in "\r\n\x00"):
            raise ValueError("Укажите допустимое имя файла MindVoice")
        if not self.content_type.isascii() or "/" not in self.content_type or any(char in self.content_type for char in "\r\n\x00"):
            raise ValueError("Укажите допустимый MIME-тип файла MindVoice")

        # Формируем служебные поля. Содержимое файла HTTPX будет читать порциями.
        fields: dict[str, str | int | bool] = {}
        if isinstance(self.recorded_at, datetime):
            if self.recorded_at.utcoffset() is None:
                raise ValueError("Укажите часовой пояс для recorded_at")
            fields["recorded_at"] = self.recorded_at.isoformat()
        elif self.recorded_at is not None:
            fields["recorded_at"] = self.recorded_at
        if self.retention_days is not None:
            fields["retention_days"] = self.retention_days
        if self.check_duplicates is not None:
            fields["check_duplicates"] = self.check_duplicates
        return fields


class _RequestOptions(TypedDict, total=False):
    """Параметры запроса, которые передаёт сгенерированная операция."""

    path: Mapping[str, _PathValue]
    query: Mapping[str, _QueryValue]
    json_query: Mapping[str, BaseModel | Sequence[BaseModel] | None]
    headers: Mapping[str, str | None]
    body: BaseModel | None
    upload: _Upload


def _client_options(api_key: str, base_url: str) -> tuple[httpx.URL, dict[str, str]]:
    """Проверяет адрес API и подготавливает заголовок авторизации Workspace."""
    if not api_key or any(not "!" <= char <= "~" for char in api_key):
        raise ValueError("Укажите допустимый API-ключ Workspace MindVoice")

    try:
        url = httpx.URL(base_url)
    except httpx.InvalidURL:
        raise ValueError("Укажите базовый HTTP(S) URL MindVoice") from None
    if url.scheme not in {"http", "https"} or not url.host or url.userinfo or "?" in base_url or "#" in base_url:
        raise ValueError("Укажите базовый HTTP(S) URL MindVoice без логина, query и фрагмента")
    return url, {"Authorization": f"Bearer {api_key}"}


def _path_segment(value: _PathValue) -> str:
    """Кодирует одно значение пути без перехода на другой маршрут."""
    segment = str(value)
    if segment in {"", ".", ".."}:
        raise ValueError("Укажите допустимый параметр пути MindVoice")
    return quote(segment, safe="")


def _query_text(value: _QueryScalar) -> str:
    """Преобразует скалярный параметр в его строковое HTTP-представление."""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _json_text(value: object) -> str:
    """Кодирует JSON для полей multipart и фильтров URL."""
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def _build_request(
    http: httpx.Client | httpx.AsyncClient,
    method: str,
    route: str,
    /,
    *,
    path: Mapping[str, _PathValue] | None = None,
    query: Mapping[str, _QueryValue] | None = None,
    json_query: Mapping[str, BaseModel | Sequence[BaseModel] | None] | None = None,
    headers: Mapping[str, str | None] | None = None,
    body: BaseModel | None = None,
    upload: _Upload | None = None,
) -> httpx.Request:
    """Собирает запрос, сохраняя повторяющиеся параметры и структуру JSON-фильтров."""
    if path:
        route = route.format_map({key: _path_segment(value) for key, value in path.items()})

    # Повторяем имя обычного массива и передаём JSON-массив одним значением.
    params: list[tuple[str, str]] = []
    for key, value in (query or {}).items():
        if isinstance(value, Sequence) and not isinstance(value, str):
            params.extend((key, _query_text(item)) for item in value)
        elif value is not None:
            params.append((key, _query_text(value)))
    for key, json_value in (json_query or {}).items():
        if isinstance(json_value, BaseModel):
            params.append((key, _json_text(json_value.model_dump(mode="json", by_alias=True, exclude_unset=True))))
        elif json_value is not None:
            items = [item.model_dump(mode="json", by_alias=True, exclude_unset=True) for item in json_value]
            params.append((key, _json_text(items)))

    request_headers = {key: value for key, value in (headers or {}).items() if value is not None}
    query_params = tuple(params)
    if upload is not None:
        # HTTPX потоково кодирует бинарную часть, сохраняя MIME-тип каждой части.
        files: dict[str, tuple[str | None, BinaryIO | str, str]] = {
            "file": (upload.filename, upload.file, upload.content_type),
        }
        if upload.metadata is not None:
            files["metadata"] = (None, _json_text(dict(upload.metadata)), "application/json")
        return http.build_request(method, route, params=query_params, headers=request_headers, data=upload.fields(), files=files)

    payload = body.model_dump(mode="json", by_alias=True, exclude_unset=True) if body is not None else None
    return http.build_request(method, route, params=query_params, headers=request_headers, json=payload)


def _decode_json(response: httpx.Response, model: type[_Response], body: bytes) -> _Response:
    """Декодирует ответ по схеме, допуская появление новых полей API."""
    try:
        return model.model_validate_json(body, extra="ignore")
    except ValidationError:
        raise ResponseError(response) from None


def _error_body(response: httpx.Response) -> bytes:
    """Читает ограниченное по размеру тело ошибки синхронного запроса."""
    try:
        body = next(response.iter_bytes(chunk_size=_MAX_ERROR_BYTES + 1), b"")
    except httpx.HTTPError:
        return b""
    return body if len(body) <= _MAX_ERROR_BYTES else b""


async def _async_error_body(response: httpx.Response) -> bytes:
    """Читает ограниченное по размеру тело ошибки асинхронного запроса."""
    try:
        body = await anext(response.aiter_bytes(chunk_size=_MAX_ERROR_BYTES + 1), b"")
    except httpx.HTTPError:
        return b""
    return body if len(body) <= _MAX_ERROR_BYTES else b""


class _AsyncUploadStream(httpx.AsyncByteStream):
    """Передаёт части multipart без чтения синхронного файла в цикле событий."""

    def __init__(self, stream: httpx.SyncByteStream) -> None:
        """Запоминает поток, собранный HTTPX."""
        self._stream = stream

    async def __aiter__(self) -> AsyncIterator[bytes]:
        """Запрашивает следующую часть только после передачи предыдущей."""
        chunks = iter(self._stream)
        while (chunk := await to_thread.run_sync(next, chunks, None)) is not None:
            yield chunk


class _SyncClient:
    """HTTP-транспорт с синхронным пулом соединений."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: httpx.Timeout | float | None = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        """Создаёт клиент с ключом Workspace, таймаутом и необязательным транспортом."""
        url, headers = _client_options(api_key, base_url)
        self._http = httpx.Client(base_url=url, headers=headers, timeout=timeout, transport=transport, follow_redirects=False)

    def __enter__(self) -> Self:
        """Открывает контекст использования клиента."""
        return self

    def __exit__(self, *exc: type[BaseException] | BaseException | TracebackType | None) -> None:
        """Закрывает пул соединений при выходе из контекста."""
        self.close()

    def close(self) -> None:
        """Закрывает клиент и его HTTP-транспорт."""
        self._http.close()

    @contextmanager
    def _stream(self, method: str, route: str, /, **options: Unpack[_RequestOptions]) -> Iterator[httpx.Response]:
        """Возвращает открытый ответ и закрывает его при любом исходе."""
        request = _build_request(self._http, method, route, **options)
        response = self._http.send(request, stream=True)
        try:
            if not response.is_success:
                raise HTTPError(response, _error_body(response))
            yield response
        finally:
            response.close()

    def _json(self, model: type[_Response], method: str, route: str, /, **options: Unpack[_RequestOptions]) -> _Response:
        """Выполняет запрос и возвращает типизированную модель ответа MindVoice."""
        with self._stream(method, route, **options) as response:
            return _decode_json(response, model, response.read())


class _AsyncClient:
    """HTTP-транспорт с асинхронным пулом соединений."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: httpx.Timeout | float | None = 30.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        """Создаёт асинхронный клиент с ключом Workspace и настройками HTTP."""
        url, headers = _client_options(api_key, base_url)
        self._http = httpx.AsyncClient(base_url=url, headers=headers, timeout=timeout, transport=transport, follow_redirects=False)

    async def __aenter__(self) -> Self:
        """Открывает асинхронный контекст использования клиента."""
        return self

    async def __aexit__(self, *exc: type[BaseException] | BaseException | TracebackType | None) -> None:
        """Закрывает пул соединений при выходе из асинхронного контекста."""
        await self.aclose()

    async def aclose(self) -> None:
        """Закрывает асинхронный клиент и его HTTP-транспорт."""
        await self._http.aclose()

    @asynccontextmanager
    async def _stream(self, method: str, route: str, /, **options: Unpack[_RequestOptions]) -> AsyncIterator[httpx.Response]:
        """Возвращает открытый ответ и закрывает его при любом исходе."""
        if "upload" in options:
            # При сборке multipart HTTPX может определять размер файла через файловые операции.
            request = await to_thread.run_sync(partial(_build_request, self._http, method, route, **options))
            request.stream = _AsyncUploadStream(cast(httpx.SyncByteStream, request.stream))
        else:
            request = _build_request(self._http, method, route, **options)

        response = await self._http.send(request, stream=True)
        try:
            if not response.is_success:
                raise HTTPError(response, await _async_error_body(response))
            yield response
        finally:
            # Освобождаем соединение и при отмене запроса на стороне приложения.
            with CancelScope(shield=True):
                await response.aclose()

    async def _json(self, model: type[_Response], method: str, route: str, /, **options: Unpack[_RequestOptions]) -> _Response:
        """Выполняет асинхронный запрос и возвращает типизированную модель ответа MindVoice."""
        async with self._stream(method, route, **options) as response:
            return _decode_json(response, model, await response.aread())
