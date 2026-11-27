"""Проверки публичного клиента MindVoice через локальный HTTPX-транспорт."""

from __future__ import annotations

import asyncio
import io
import json
import threading
from collections.abc import AsyncIterator, Iterator
from datetime import UTC, datetime
from email import policy
from email.parser import BytesParser
from inspect import signature
from pathlib import Path
from typing import Any
from uuid import UUID

import httpx
import pytest
import yaml
from anyio import CancelScope, sleep
from pydantic import TypeAdapter

from mindvoice import AsyncClient, Client, HTTPError, ResponseError, models

WORKSPACE = "ws-550e8400-e29b-41d4-a716-446655440000"
RECORDING = "fl-550e8400-e29b-41d4-a716-446655440000"
RUN = "trn-550e8400-e29b-41d4-a716-446655440000"
KEY = "ws-sk-test"
LARGE_INTEGER = 2**70 + 17
RECORDED_AT = "2026-09-30T10:00:00Z"


def _workspace_payload() -> dict[str, Any]:
    """Возвращает карточку пространства в формате публичного API."""
    return {
        "workspaces": [
            {
                "id": WORKSPACE,
                "name": "Рабочее пространство",
                "access": {"role": "owner", "is_default": False, "new_field": "Новое поле"},
                "audit": {"created_at": RECORDED_AT},
            }
        ]
    }


def _recording_payload() -> dict[str, Any]:
    """Возвращает запись с обязательными полями и произвольными метаданными."""
    return {
        "id": RECORDING,
        "source": "API",
        "metadata": {"external_id": LARGE_INTEGER, "nested": [False, "", None]},
        "file": {"filename": "recording.mp3", "checksum_algorithm": "sha256"},
        "storage": {"uploaded_at": RECORDED_AT},
        "processing": {"status": "completed"},
        "statistics": {"transcriptions_count": 0, "analyses_count": 0},
    }


def test_operations_have_matching_parameters() -> None:
    """Сверяет все закреплённые операции и аргументы двух клиентов."""
    manifest = Path(__file__).resolve().parents[1] / "openapi" / "operations.yaml"
    operations = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    expected = {operation["name"] for operation in operations.values()}
    assert len(expected) == 43
    for client in (Client, AsyncClient):
        assert {name for name in vars(client) if not name.startswith("_")} == expected
    for name in expected:
        assert signature(getattr(Client, name)).parameters == signature(getattr(AsyncClient, name)).parameters


def test_workspace_authorization_and_response() -> None:
    """Проверяет публичный адрес, заголовок ключа и декодирование новых полей."""

    def handle(request: httpx.Request) -> httpx.Response:
        """Возвращает список доступных пространств."""
        assert request.method == "GET"
        assert str(request.url) == "https://api.mindvoice.pro/v1/workspaces"
        assert request.headers["Authorization"] == f"Bearer {KEY}"
        return httpx.Response(200, json=_workspace_payload())

    with Client(KEY, transport=httpx.MockTransport(handle)) as client:
        (workspace,) = client.list_workspaces().workspaces
    assert isinstance(workspace, models.WorkspaceItem)
    assert workspace.id == WORKSPACE
    assert workspace.access.is_default is False
    assert workspace.audit.created_at == datetime(2026, 9, 30, 10, tzinfo=UTC)


@pytest.mark.parametrize("bad_key", ["", "a b", "a\nb", "кириллица"])
def test_invalid_api_key(bad_key: str) -> None:
    """Отклоняет недопустимые значения заголовка авторизации при создании."""
    with pytest.raises(ValueError, match="API-ключ"):
        Client(bad_key)


@pytest.mark.parametrize("url", ["relative/path", "ftp://api.test", "https://user@api.test", "https://api.test?x=1", "https://api.test#"])
def test_invalid_base_url(url: str) -> None:
    """Отклоняет адреса неподдерживаемого формата при создании."""
    with pytest.raises(ValueError, match="URL"):
        Client(KEY, base_url=url)


def test_recording_filters_and_response_values() -> None:
    """Передаёт повторяющиеся параметры, отрицание и вложенные JSON-фильтры."""

    def handle(request: httpx.Request) -> httpx.Response:
        """Проверяет query после URL-кодирования и возвращает страницу записей."""
        assert request.url.path == f"/proxy/v1/workspaces/{WORKSPACE}/recordings"
        params = request.url.params
        assert params.get_list("status") == ["completed", "failed"]
        assert params["offset"] == "0"
        assert params["only_without_transcription"] == "false"
        assert params["uploaded_from"] == "2026-09-30"
        assert "page_size" not in params
        assert json.loads(params["metadata_filters"]) == [
            {"field": "external_id", "operator": "equals", "value": LARGE_INTEGER},
            {"field": "unset", "operator": "exists"},
            {"field": "present", "operator": "equals", "value": None},
        ]
        assert json.loads(params["metadata_group"]) == {
            "logic": "or",
            "conditions": [{"conditions": [{"field": "nested", "operator": "equals", "value": False}]}],
        }
        return httpx.Response(
            200,
            json={
                "recordings": [_recording_payload()],
                "pagination": {"page_size": 50, "offset": 0, "total_count": 1},
                "statistics": {"total_count": "1", "total_size_bytes": "0", "total_duration_seconds": 0.0, "status_counts": {}},
            },
        )

    group = models.MetadataGroup(
        logic="or",
        conditions=[models.MetadataGroup(conditions=[models.MetadataFilter(field="nested", operator="equals", value=False)])],
    )
    with Client(KEY, base_url="https://api.test/proxy", transport=httpx.MockTransport(handle)) as client:
        result = client.list_recordings(
            WORKSPACE,
            offset=0,
            only_without_transcription=False,
            status=("completed", "failed"),
            uploaded_from="2026-09-30",
            metadata_filters=[
                models.MetadataFilter(field="external_id", operator="equals", value=LARGE_INTEGER),
                models.MetadataFilter(field="unset", operator="exists"),
                models.MetadataFilter(field="present", operator="equals", value=None),
            ],
            metadata_group=group,
        )
    assert result.recordings[0].metadata == _recording_payload()["metadata"]
    assert result.pagination.offset == 0


def test_json_request_fields() -> None:
    """Проверяет типизированное тело импорта и сохранение явно переданных значений."""

    def handle(request: httpx.Request) -> httpx.Response:
        """Проверяет JSON и возвращает результат постановки в очередь."""
        assert request.method == "POST"
        assert request.url.path == f"/v1/workspaces/{WORKSPACE}/recordings/import"
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.content) == {
            "file": {"url": "https://storage.test/call.mp3", "filename": "call.mp3"},
            "check_duplicates": False,
            "metadata": {"empty": None, "number": LARGE_INTEGER},
        }
        return httpx.Response(202, json={"recording": _recording_payload()})

    with Client(KEY, transport=httpx.MockTransport(handle)) as client:
        response = client.import_recording(
            WORKSPACE,
            models.RecordingImport(
                file=models.RecordingImportFile(url="https://storage.test/call.mp3", filename="call.mp3"),
                check_duplicates=False,
                metadata={"empty": None, "number": LARGE_INTEGER},
            ),
        )
    assert response.recording.id == RECORDING


class _Audio(io.BytesIO):
    """Файл, который фиксирует размер и поток каждого чтения."""

    def __init__(self, content: bytes) -> None:
        """Сохраняет аудиоданные и подготавливает журнал чтений."""
        super().__init__(content)
        self.reader_threads: list[int] = []

    def read(self, size: int = -1) -> bytes:
        """Проверяет, что загрузка запрашивает ограниченную порцию аудио."""
        assert 0 < size <= 64 * 1024
        self.reader_threads.append(threading.get_ident())
        return super().read(size)


@pytest.mark.parametrize("asynchronous", [False, True])
def test_multipart_audio_upload(asynchronous: bool) -> None:
    """Передаёт аудио порциями и сохраняет типы, нулевые значения и владение файлом."""
    content = b"mp3" * 100_000
    audio = _Audio(content)

    def handle(request: httpx.Request) -> httpx.Response:
        """Разбирает multipart как сообщение с типизированными частями."""
        assert request.method == "POST"
        assert request.url.path == f"/v1/workspaces/{WORKSPACE}/recordings"
        header = request.headers["Content-Type"]
        multipart = BytesParser(policy=policy.default).parsebytes(f"Content-Type: {header}\r\n\r\n".encode() + request.content)
        parts = {part.get_param("name", header="content-disposition"): part for part in multipart.iter_parts()}
        assert parts["file"].get_filename() == "звонок.mp3"
        assert parts["file"].get_content_type() == "audio/mpeg"
        assert parts["file"].get_payload(decode=True) == content
        assert parts["metadata"].get_content_type() == "application/json"
        assert json.loads(parts["metadata"].get_payload(decode=True)) == {"number": LARGE_INTEGER, "empty": None}
        assert parts["check_duplicates"].get_payload() == "false"
        assert parts["recorded_at"].get_payload() == "2026-09-30T10:00:00+00:00"
        assert parts["retention_days"].get_payload() == "30"
        return httpx.Response(200, json={"recording": _recording_payload()})

    async def upload() -> models.RecordingItemResponse:
        """Загружает файл из асинхронного приложения."""
        async with AsyncClient(KEY, transport=httpx.MockTransport(handle)) as client:
            return await client.upload_recording(
                WORKSPACE,
                file=audio,
                filename="звонок.mp3",
                content_type="audio/mpeg",
                metadata={"number": LARGE_INTEGER, "empty": None},
                check_duplicates=False,
                recorded_at=datetime(2026, 9, 30, 10, tzinfo=UTC),
                retention_days=30,
            )

    with audio:
        if asynchronous:
            response = asyncio.run(upload())
            assert threading.get_ident() not in audio.reader_threads
        else:
            with Client(KEY, transport=httpx.MockTransport(handle)) as client:
                response = client.upload_recording(
                    WORKSPACE,
                    file=audio,
                    filename="звонок.mp3",
                    content_type="audio/mpeg",
                    metadata={"number": LARGE_INTEGER, "empty": None},
                    check_duplicates=False,
                    recorded_at=datetime(2026, 9, 30, 10, tzinfo=UTC),
                    retention_days=30,
                )
        assert not audio.closed
        assert len(audio.reader_threads) > 2
    assert response.recording.id == RECORDING


class _FileBody(httpx.SyncByteStream, httpx.AsyncByteStream):
    """Файловый ответ, фиксирующий первый запрос содержимого и закрытие."""

    def __init__(self) -> None:
        """Подготавливает счётчики чтения и закрытия."""
        self.read = False
        self.closed = False

    def __iter__(self) -> Iterator[bytes]:
        """Возвращает аудиофрагмент только после обращения к потоку."""
        self.read = True
        yield b"audio"

    async def __aiter__(self) -> AsyncIterator[bytes]:
        """Асинхронно возвращает аудиофрагмент по запросу."""
        self.read = True
        yield b"audio"

    def close(self) -> None:
        """Фиксирует освобождение синхронного потока."""
        self.closed = True

    async def aclose(self) -> None:
        """Фиксирует освобождение асинхронного потока."""
        self.closed = True


def test_range_download_is_streamed_and_closed() -> None:
    """Сохраняет параметры Range, метаданные и ленивое чтение тела."""
    stream = _FileBody()

    def handle(request: httpx.Request) -> httpx.Response:
        """Возвращает запрошенный диапазон исходного файла."""
        assert request.url.path.endswith(f"/recordings/{RECORDING}/download")
        assert request.headers["Range"] == "bytes=0-4"
        assert request.headers["If-Range"] == '"etag"'
        return httpx.Response(206, headers={"Content-Range": "bytes 0-4/7"}, stream=stream)

    with Client(KEY, transport=httpx.MockTransport(handle)) as client:
        with client.download_recording(WORKSPACE, RECORDING, range="bytes=0-4", if_range='"etag"') as response:
            assert response.status_code == 206
            assert response.headers["Content-Range"] == "bytes 0-4/7"
            assert not stream.read
        assert stream.closed
        assert not stream.read


def test_async_json_and_transcript_export() -> None:
    """Проверяет JSON и экспорт текста расшифровки в одном асинхронном клиенте."""
    stream = _FileBody()

    async def handle(request: httpx.Request) -> httpx.Response:
        """Возвращает список пространств или файл экспорта."""
        if request.url.path == "/v1/workspaces":
            return httpx.Response(200, json=_workspace_payload())
        assert request.url.path.endswith(f"/transcription-runs/{RUN}/transcript/export")
        assert request.url.params["format"] == "vtt"
        return httpx.Response(200, stream=stream)

    async def run() -> None:
        """Читает поток экспорта только при входе в контекст скачивания."""
        async with AsyncClient(KEY, transport=httpx.MockTransport(handle)) as client:
            assert (await client.list_workspaces()).workspaces[0].id == WORKSPACE
            async with client.export_transcript(WORKSPACE, RUN, format="vtt") as response:
                assert not stream.read
                assert [part async for part in response.aiter_bytes()] == [b"audio"]
            assert stream.closed

    asyncio.run(run())


def test_api_error_contains_status_and_domain_details() -> None:
    """Разбирает доменную ошибку, поля и служебные заголовки ответа."""
    body = {
        "error": {
            "code": "invalid_argument",
            "message": "Некорректный запрос",
            "violations": [{"field_path": "page_size", "code": "limit", "message": "Слишком много"}],
            "details": {"number": LARGE_INTEGER},
            "request_id": "body-id",
        }
    }
    transport = httpx.MockTransport(
        lambda _: httpx.Response(422, json=body, headers={"Retry-After": "5", "X-Request-ID": "header-id"}),
    )
    with Client(KEY, transport=transport) as client, pytest.raises(HTTPError) as caught:
        client.list_workspaces()
    error = caught.value
    assert error.status_code == 422
    assert error.request_id == "body-id"
    assert error.retry_after == "5"
    assert error.code == "invalid_argument"
    assert error.violations[0].field_path == "page_size"
    assert error.details == {"number": LARGE_INTEGER}


def test_unstructured_file_error() -> None:
    """Сохраняет HTTP-статус и размер исходного файла при ответе 416 без JSON."""
    transport = httpx.MockTransport(lambda _: httpx.Response(416, headers={"Content-Range": "bytes */7", "X-Request-ID": "ref"}))
    with Client(KEY, transport=transport) as client, pytest.raises(HTTPError) as caught:
        with client.download_recording(WORKSPACE, RECORDING, range="bytes=99-"):
            pytest.fail("Ожидалась ошибка диапазона")
    assert caught.value.status_code == 416
    assert caught.value.request_id == "ref"
    assert caught.value.content_range == "bytes */7"
    assert caught.value.code is None


def test_async_error_limits_body_and_closes_stream() -> None:
    """Прерывает чтение длинного ответа прокси и освобождает асинхронный поток."""

    class ProxyBody(_FileBody):
        """Поток прокси, который нельзя дочитывать целиком."""

        async def __aiter__(self) -> AsyncIterator[bytes]:
            """Возвращает данные сверх лимита обработки ошибок API."""
            yield b"a" * (64 * 1024 + 1)
            pytest.fail("Тело ошибки прочитано сверх лимита")

    stream = ProxyBody()
    transport = httpx.MockTransport(lambda _: httpx.Response(502, stream=stream, headers={"X-Request-ID": "proxy"}))

    async def run() -> None:
        """Проверяет статус и освобождение тела при ошибке API."""
        async with AsyncClient(KEY, transport=transport) as client:
            with pytest.raises(HTTPError) as caught:
                await client.list_workspaces()
            assert caught.value.status_code == 502
            assert caught.value.request_id == "proxy"
            assert caught.value.code is None
            assert stream.closed

    asyncio.run(run())


def test_async_cancelled_download_closes_stream() -> None:
    """Закрывает поток скачивания при отмене вызывающей операции."""

    class CancelledBody(_FileBody):
        """Поток с асинхронным освобождением ресурса."""

        async def aclose(self) -> None:
            """Освобождает ресурс даже при отменённом внешнем контексте."""
            await sleep(0)
            self.closed = True

    stream = CancelledBody()
    transport = httpx.MockTransport(lambda _: httpx.Response(200, stream=stream))

    async def run() -> None:
        """Отменяет скачивание внутри открытого ответа."""
        async with AsyncClient(KEY, transport=transport) as client:
            with CancelScope() as scope:
                async with client.download_recording(WORKSPACE, RECORDING):
                    scope.cancel()
                    await sleep(0)
            assert stream.closed

    asyncio.run(run())


def test_redirect_does_not_send_key_again() -> None:
    """Отклоняет перенаправление и оставляет ключ у исходного запроса."""
    destinations = []

    def handle(request: httpx.Request) -> httpx.Response:
        """Предлагает перенаправление на другой хост."""
        destinations.append(request.url.host)
        return httpx.Response(307, headers={"Location": "https://redirect.test/api"})

    with Client(KEY, transport=httpx.MockTransport(handle)) as client, pytest.raises(HTTPError) as caught:
        client.list_workspaces()
    assert caught.value.status_code == 307
    assert destinations == ["api.mindvoice.pro"]


def test_invalid_success_response_does_not_include_body() -> None:
    """Возвращает ошибку схемы с техническим идентификатором без тела."""
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json={"workspaces": "details"}, headers={"X-Request-ID": "ref"}))
    with Client(KEY, transport=transport) as client, pytest.raises(ResponseError) as caught:
        client.list_workspaces()
    assert caught.value.status_code == 200
    assert caught.value.request_id == "ref"
    assert "details" not in str(caught.value)


def test_uuid_paths_and_encoded_segments() -> None:
    """Оставляет UUID в стандартном формате и кодирует разделители одного сегмента."""

    def handle(request: httpx.Request) -> httpx.Response:
        """Возвращает HTTP-ошибку, чтобы проверить только построение URL."""
        raw_path = request.url.raw_path
        assert b"/analysis-results/550e8400-e29b-41d4-a716-446655440000" in raw_path or b"/x%2Fy%3Fz/versions/1" in raw_path
        return httpx.Response(404)

    with Client(KEY, transport=httpx.MockTransport(handle)) as client:
        with pytest.raises(HTTPError):
            client.get_analysis_result(WORKSPACE, UUID("550e8400-e29b-41d4-a716-446655440000"))
        with pytest.raises(HTTPError):
            client.get_analysis_criterion_template_version(WORKSPACE, "x/y?z", 1)
        with pytest.raises(ValueError, match="параметр пути"):
            client.get_analysis_criterion_template_version(WORKSPACE, "..", 1)


@pytest.mark.parametrize("wire", [{"boolean_value": False}, {"text_value": ""}, {"selected_options": {"options": []}}])
def test_answer_value_preserves_empty_and_false(wire: dict[str, Any]) -> None:
    """Сохраняет пустой текст, отрицательный ответ и пустой выбор критериев."""
    adapter = TypeAdapter(models.AnswerValue)
    value = adapter.validate_python(wire)
    assert adapter.dump_python(value, exclude_unset=True) == wire
