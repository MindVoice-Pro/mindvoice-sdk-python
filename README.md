# MindVoice SDK для Python

Клиент публичного API MindVoice для Python 3.11 и новее. SDK поддерживает
43 операции с ключом Workspace, включая загрузку аудио, транскрибацию, анализ и
скачивание результатов. По умолчанию клиент обращается к `https://api.mindvoice.pro`.

[Портал разработчиков MindVoice](https://developer.mindvoice.pro/) ·
[Справочник API](https://developer.mindvoice.pro/api-reference/)

## Установка

Установите пакет с PyPI.

```bash
python -m pip install mindvoice-sdk
```

Имя дистрибутива — `mindvoice-sdk`, имя модуля — `mindvoice`.
Для установки из исходников выполните `python -m pip install .` в каталоге репозитория.

## Первый запрос

Создайте API-ключ в настройках Workspace и передайте его через переменную
окружения `MINDVOICE_API_KEY`. SDK добавит заголовок `Authorization: Bearer …`.
[Получение ключа и выбор прав](https://developer.mindvoice.pro/docs/getting-started/authentication/)

```python
import os

from mindvoice import Client

with Client(os.environ["MINDVOICE_API_KEY"]) as client:
    for workspace in client.list_workspaces().workspaces:
        print(workspace.id, workspace.name)
```

`Client` и `AsyncClient` используют пул соединений. Переиспользуйте экземпляр
для запросов с одним ключом и закрывайте его через `with` или `async with`.
Параметр `base_url` задаёт адрес доверенной тестовой среды или прокси,
`timeout` — таймаут HTTPX, по умолчанию 30 секунд на этап сетевого ввода-вывода.
Собственный HTTPX-транспорт можно передать через `transport`.

## Асинхронный клиент

```python
import asyncio
import os

from mindvoice import AsyncClient


async def main() -> None:
    """Выводит пространства, доступные ключу Workspace."""
    async with AsyncClient(os.environ["MINDVOICE_API_KEY"]) as client:
        result = await client.list_workspaces()
        for workspace in result.workspaces:
            print(workspace.id, workspace.name)


asyncio.run(main())
```

## Загрузка и импорт аудио

`upload_recording` читает открытый бинарный файл порциями. Закрывайте файл в
вызывающем коде. Укажите имя с расширением и MIME-тип, например `audio/mpeg`
для MP3 или `audio/wav` для WAV.

```python
from pathlib import Path

from mindvoice import Client


def upload_mp3(client: Client, workspace_id: str, path: Path) -> str:
    """Загружает локальный MP3 и возвращает ID записи."""
    with path.open("rb") as audio:
        result = client.upload_recording(
            workspace_id,
            file=audio,
            filename=path.name,
            content_type="audio/mpeg",
            metadata={"external_id": "call-123"},
        )
    return result.recording.id
```

Можно передать `recorded_at` как `datetime` с часовым поясом или строку RFC 3339,
`retention_days` и `check_duplicates`. По умолчанию API проверяет дубликаты.
Ключи верхнего уровня `metadata` должны соответствовать `[a-z0-9_]{1,64}`.
[Форматы аудио и метаданные](https://developer.mindvoice.pro/docs/guides/upload-and-results/)

Для импорта из хранилища передайте прямую ссылку на аудио, доступную MindVoice.
Ответ содержит ID записи после постановки импорта в очередь.

```python
from mindvoice import Client, models


def import_mp3(client: Client, workspace_id: str, url: str) -> str:
    """Ставит импорт аудио по прямой ссылке в очередь."""
    result = client.import_recording(
        workspace_id,
        models.RecordingImport(file=models.RecordingImportFile(url=url, filename="call.mp3")),
    )
    return result.recording.id
```

Оба метода требуют `recordings:write`. Для проверки статуса и скачивания нужен
`recordings:read`. Вызывайте `get_recording(workspace_id, recording_id)` до
завершения подготовки. Статус `recording.processing.status == "completed"`
означает, что аудио готово к ручному запуску сценария.

## Транскрибация и анализ

Если сценарии уже запускаются автоматически, найдите их запуски через
`list_transcription_runs` и `list_analysis_runs` с фильтром `recording_id`.
Для ручных запусков выберите нужный сценарий из `list_transcription_scenarios`
или `list_analysis_scenarios`. Сохраните ID запуска, чтобы проверять его статус.

```python
from mindvoice import Client, models


def start_transcription(client: Client, workspace_id: str, recording_id: str, scenario_id: str) -> str:
    """Запускает транскрибацию подготовленного аудио по выбранному сценарию."""
    result = client.start_transcription_run(
        workspace_id,
        recording_id,
        models.TranscriptionRunCreate(transcription_scenario_id=scenario_id),
    )
    return result.run.id
```

Проверяйте `get_transcription_run(workspace_id, run_id).run.execution.status`
с паузой между запросами и ограничением общего времени ожидания. При
`completed` вызовите `get_transcript(workspace_id, run_id)`. Сегменты находятся
в `transcript.content.segments`, а `transcript.id` указывает на конкретную версию
текста расшифровки. При `failed` или `cancelled` завершите ожидание и проверьте
состояние запуска.

```python
from mindvoice import Client, models


def start_analysis(
    client: Client, workspace_id: str, recording_id: str, scenario_id: str, transcript_id: str
) -> str:
    """Запускает анализ конкретной версии текста расшифровки."""
    result = client.start_analysis_run(
        workspace_id,
        recording_id,
        models.AnalysisRunCreate(analysis_scenario_id=scenario_id, transcript_id=transcript_id),
    )
    return result.run.id
```

Проверяйте `get_analysis_run(workspace_id, run_id).run.execution.status`. После
`completed` получите результат через
`get_recording_analysis_result(workspace_id, recording_id, run_id)`.
Ответы на критерии доступны в `result.result.answers`, резюме — в
`result.result.summary`.

Для чтения сценариев, запусков и результатов нужны `transcripts:read` или
`analysis:read` соответственно. Ручные запуски требуют `transcripts:write` или
`analysis:write`.
[Сценарии транскрибации и анализа](https://developer.mindvoice.pro/docs/guides/scenarios/)

## Скачивание

`download_recording` возвращает поток исходного аудио. Параметры `range` и
`if_range` передаются HTTP-заголовками. Для частичного ответа проверяйте
`response.status_code == 206` и `response.headers["Content-Range"]`.

`export_transcript` поддерживает `srt`, `vtt`, `txt` и `txt_timestamps`. Оба
метода возвращают контекстный менеджер с потоковым ответом HTTPX. Читайте его
внутри `with` через `iter_bytes()`, а с `AsyncClient` — внутри `async with`
через `aiter_bytes()`.

```python
from pathlib import Path

from mindvoice import Client


def export_srt(client: Client, workspace_id: str, run_id: str, destination: Path) -> None:
    """Сохраняет экспорт субтитров порциями."""
    with client.export_transcript(workspace_id, run_id, format="srt") as response:
        with destination.open("wb") as output:
            for chunk in response.iter_bytes():
                output.write(chunk)
```

[Скачивание файлов и форматы экспорта](https://developer.mindvoice.pro/docs/guides/upload-and-results/)

## Фильтры и пагинация

Передавайте фильтры именованными аргументами. Например,
`list_recordings(workspace_id, status=["completed", "failed"])` передаёт два
значения `status`. Структуры `models.MetadataFilter` и `models.MetadataGroup`
передаются в `metadata_filters` и `metadata_group` соответственно.

```python
from collections.abc import Iterator

from mindvoice import Client, models


def iter_recordings(client: Client, workspace_id: str) -> Iterator[models.RecordingItem]:
    """Перебирает записи, сохраняя фильтры и размер страницы."""
    offset = 0
    while True:
        page = client.list_recordings(workspace_id, page_size=50, offset=offset, status=["completed"])
        if not page.recordings:
            break
        yield from page.recordings
        offset += len(page.recordings)
        total = page.pagination.total_count
        if total is not None and offset >= total:
            break
```

[Пагинация и параметры списков](https://developer.mindvoice.pro/docs/guides/pagination/)

## Ошибки и повторы

Для HTTP-ошибок перехватывайте `mindvoice.HTTPError`. Используйте
`status_code` и `code` для ветвления, `violations` для ошибок полей,
`request_id` для обращения в поддержку, `retry_after` для обработки
ограничений частоты. Ответ `416` может содержать `content_range`.

Некорректное тело успешного ответа вызывает `mindvoice.ResponseError`.
Сетевые ошибки и таймауты передаются как исключения HTTPX. Перенаправления
возвращаются как HTTP-ошибки. После сетевого сбоя при загрузке или запуске
сначала проверьте состояние операции. Повторами управляет вызывающее
приложение.
[Обработка ошибок API](https://developer.mindvoice.pro/docs/guides/error-handling/)

## Для сопровождающих SDK

В каталоге репозитория выполните:

```bash
uv sync --locked
uv run --locked python scripts/generate.py
uv run --locked python scripts/generate.py --check
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src
uv build
```

Генератор читает [опубликованный OpenAPI](https://developer.mindvoice.pro/openapi.yaml)
и обновляет `src/mindvoice/models.py` и `src/mindvoice/_operations.py`.
Для локальной копии контракта передайте `--spec путь/к/openapi.yaml`.
В [operations.yaml](openapi/operations.yaml) закреплены публичные имена и
описания методов. При добавлении или удалении маршрутов обновите этот
файл, перегенерируйте SDK и проверьте diff.

### Публикация на PyPI

[Workflow публикации](.github/workflows/publish-pypi.yml) запускается после
публикации GitHub Release. Он сверяет тег с версией пакета, запускает проверки,
собирает wheel и архив исходников, затем загружает их на PyPI через Trusted
Publishing (OIDC).

Перед первым релизом владелец аккаунта PyPI добавляет ожидающего издателя
(*pending publisher*) на странице [Publishing](https://pypi.org/manage/account/publishing/).
В разделе GitHub Actions укажите:

| Поле | Значение |
| --- | --- |
| PyPI Project Name | `mindvoice-sdk` |
| Owner | `MindVoice-Pro` |
| Repository name | `mindvoice-sdk-python` |
| Workflow name | `publish-pypi.yml` |
| Environment name | `pypi` |

PyPI создаст проект при первом успешном запуске. Если проект уже существует,
его владелец добавляет издателя с теми же параметрами в разделе **Manage →
Publishing** проекта. Для OIDC достаточно этой привязки, секрет с API-токеном
PyPI не требуется. [Настройка первого издателя на PyPI](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)

1. Укажите версию в `pyproject.toml` и обновите `uv.lock` командой `uv lock`.
2. Опубликуйте GitHub Release с тегом вида `v0.1.0` на коммите с этой версией
   пакета и файлом workflow. Для предварительного релиза используйте версию
   PEP 440, например `0.2.0rc1`, и тег `v0.2.0rc1`.
3. Проверьте запуск в **Actions**. После успешной публикации пакет доступен
   для установки командой `python -m pip install mindvoice-sdk`.
