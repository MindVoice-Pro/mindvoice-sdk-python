"""Генерирует операции и модели Python SDK по опубликованному OpenAPI MindVoice."""

from __future__ import annotations

import argparse
import json
import keyword
import re
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
from urllib.request import urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://developer.mindvoice.pro/openapi.yaml"
OPERATIONS = ROOT / "openapi" / "operations.yaml"
OUTPUT = Path("src/mindvoice")
HTTP_METHODS = {"delete", "get", "head", "options", "patch", "post", "put", "trace"}
GENERATED = "# Сгенерировано из OpenAPI MindVoice командой uv run python scripts/generate.py.\n"
Schema = dict[str, Any]


def _ref_name(schema: Schema) -> str:
    """Возвращает имя Python для ссылки на модель из components.schemas."""
    ref = schema.get("$ref", "")
    match = re.fullmatch(r"#/components/schemas/([\w-]+)", ref)
    if match is None:
        raise ValueError(f"Ожидалась ссылка на именованную модель: {schema}")
    return match[1].replace("-", "")


def _literal(values: list[str]) -> str:
    """Преобразует допустимые значения OpenAPI в аннотацию Literal."""
    return f"Literal[{', '.join(map(repr, values))}]"


def _parameter_type(schema: Schema) -> str:
    """Сопоставляет схему URL-параметра с типом аргумента Python."""
    if "$ref" in schema:
        model = _ref_name(schema)
        return "str" if model == "DateBoundary" else f"models.{model}"
    if "enum" in schema:
        return _literal(schema["enum"])
    if schema.get("format") == "uuid":
        return "str | UUID"
    if schema.get("type") == "array":
        return f"Sequence[{_parameter_type(schema['items'])}]"
    return {"string": "str", "integer": "int", "number": "float", "boolean": "bool", "null": "None"}[schema["type"]]


def _upload_arguments(operation: Schema) -> list[str]:
    """Проверяет контракт файла и задаёт аргументы потокового метода загрузки."""
    if set(operation["properties"]) != {"file", "metadata", "retention_days", "recorded_at", "check_duplicates"}:
        raise ValueError("Изменились поля multipart. Обновите потоковую загрузку SDK.")
    if operation["required"] != ["file"] or operation["properties"]["file"].get("format") != "binary":
        raise ValueError("Изменились обязательные поля multipart. Обновите потоковую загрузку SDK.")
    return [
        "file: BinaryIO",
        "filename: str",
        "content_type: str",
        "metadata: Mapping[str, JsonValue] | None = None",
        "recorded_at: datetime | str | None = None",
        "retention_days: int | None = None",
        "check_duplicates: bool | None = None",
    ]


def _render_method(
    method: str,
    route: str,
    operation: Schema,
    naming: dict[str, str],
    schemas: dict[str, Schema],
    transcript_formats: list[str],
    *,
    asynchronous: bool,
) -> str:
    """Генерирует сигнатуру операции и передачу её параметров HTTP-транспорту."""
    name = naming["name"]
    positional = ["self"]
    named: list[str] = []
    options: dict[str, list[str]] = {}
    extra_options: list[str] = []

    # Разделяем обычные query-параметры, JSON-фильтры и HTTP-заголовки.
    for parameter in operation.get("parameters", []):
        wire_name = parameter["name"]
        argument = wire_name.lower().replace("-", "_")
        required = parameter.get("required", False)
        location = parameter["in"]
        if "content" in parameter:
            if location != "query" or set(parameter["content"]) != {"application/json"}:
                raise ValueError(f"Неподдерживаемое содержимое параметра {wire_name}")
            type_name = _parameter_type(parameter["content"]["application/json"]["schema"])
            location = "json_query"
        else:
            type_name = _parameter_type(parameter["schema"])
        if name == "export_transcript" and wire_name == "format":
            transcript_formats[:] = parameter["schema"]["enum"]
            type_name = "TranscriptFormat"

        if location not in {"path", "query", "json_query", "header"}:
            raise ValueError(f"Неподдерживаемое расположение параметра {wire_name}: {location}")
        target = positional if location == "path" else named
        option_name = "headers" if location == "header" else location
        target.append(f"{argument}: {type_name}" + ("" if required else " | None = None"))
        options.setdefault(option_name, []).append(f"{wire_name!r}: {argument}")

    # JSON-тело передаётся моделью; для multipart используется открытый бинарный файл.
    if request := operation.get("requestBody"):
        content = request["content"]
        if set(content) == {"application/json"}:
            type_name = _ref_name(content["application/json"]["schema"])
            annotation = f"body: models.{type_name}"
            positional.append(annotation if request["required"] else f"{annotation} | None = None")
            extra_options.append("body=body")
        elif set(content) == {"multipart/form-data"} and name == "upload_recording":
            model = _ref_name(content["multipart/form-data"]["schema"])
            named.extend(_upload_arguments(schemas[model]))
            extra_options.append("upload=_Upload(file, filename, content_type, metadata, recorded_at, retention_days, check_duplicates)")
        else:
            raise ValueError(f"Неподдерживаемое тело запроса: {name}")

    # Для файловых ответов вызывающая сторона управляет временем жизни потока.
    response_content = {
        mime: definition.get("schema", {})
        for status, response in operation["responses"].items()
        if status.startswith("2")
        for mime, definition in response.get("content", {}).items()
    }
    call_args = [repr(method), repr(route)]
    if set(response_content) == {"application/json"}:
        result = f"models.{_ref_name(response_content['application/json'])}"
        call_args.insert(0, result)
        prefix = "await self._json" if asynchronous else "self._json"
    elif response_content and all(schema.get("format") == "binary" for schema in response_content.values()):
        result = "AbstractAsyncContextManager[httpx.Response]" if asynchronous else "AbstractContextManager[httpx.Response]"
        prefix = "self._stream"
    else:
        raise ValueError(f"Неподдерживаемый успешный ответ: {name}")
    signature = [*positional, "*", *named] if named else positional
    call_args += [f"{key}={{{', '.join(values)}}}" for key, values in options.items()]
    call_args += extra_options
    call = ",\n            ".join(call_args)
    definition = "async def" if prefix.startswith("await ") else "def"
    return (
        f"    {definition} {name}({', '.join(signature)}) -> {result}:\n"
        f'        """{naming["summary"]}"""\n'
        f"        return {prefix}(\n            {call},\n        )\n"
    )


def _render_operations(spec: Schema, names: dict[str, dict[str, str]]) -> str:
    """Генерирует одинаковый набор операций для синхронного и асинхронного клиентов."""
    operations = {}
    for route, path_item in spec["paths"].items():
        for method, operation in path_item.items():
            if method in HTTP_METHODS:
                operations[f"{method.upper()} {route}"] = operation
    missing = operations.keys() - names.keys()
    stale = names.keys() - operations.keys()
    if missing or stale:
        raise ValueError(f"Сверьте openapi/operations.yaml: новые операции {sorted(missing)}, удалённые {sorted(stale)}")
    method_names = [item["name"] for item in names.values()]
    if len(set(method_names)) != len(method_names) or any(
        not name.isidentifier() or keyword.iskeyword(name) or name.startswith("_") for name in method_names
    ):
        raise ValueError("Публичные имена операций должны быть различными идентификаторами Python")

    # Формат экспорта берём из контракта, а не дублируем список значений вручную.
    formats: list[str] = []
    classes = []
    for name, base, description in (
        ("Client", "_SyncClient", "Синхронный клиент публичного API MindVoice."),
        ("AsyncClient", "_AsyncClient", "Асинхронный клиент публичного API MindVoice."),
    ):
        methods = []
        for key, naming in names.items():
            method, route = key.split(" ", 1)
            methods.append(
                _render_method(
                    method, route, operations[key], naming, spec["components"]["schemas"], formats, asynchronous=name == "AsyncClient"
                )
            )
        classes.append(f'class {name}({base}):\n    """{description}"""\n\n' + "\n".join(methods))
    if not formats:
        raise ValueError("В контракте отсутствуют допустимые форматы экспорта")

    return (
        GENERATED
        + '''"""Типизированные операции публичного API MindVoice."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from datetime import datetime
from typing import BinaryIO, Literal
from uuid import UUID

import httpx
from pydantic import JsonValue

from . import models
from ._transport import _AsyncClient, _SyncClient, _Upload

'''
        + f"TranscriptFormat = {_literal(formats)}\n\n\n"
        + "\n\n".join(classes)
    )


def _generate_models(source: Path, output: Path) -> None:
    """Строит модели Pydantic, используя нативные типы для JSON-значений."""
    options = [
        "--input",
        str(source),
        "--input-file-type",
        "openapi",
        "--output",
        str(output),
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.11",
        "--enum-field-as-literal",
        "all",
        "--use-standard-collections",
        "--use-union-operator",
        "--snake-case-field",
        "--allow-population-by-field-name",
        "--use-schema-description",
        "--use-field-description",
        "--use-annotated",
        "--use-type-alias-type",
        "--type-overrides",
        json.dumps({"JsonValue": "pydantic.JsonValue", "DateBoundary": "builtins.str"}),
        "--disable-timestamp",
        "--formatters",
        "builtin",
        "--custom-file-header",
        GENERATED.strip(),
    ]
    subprocess.run([sys.executable, "-m", "datamodel_code_generator", *options], check=True)


def _read_source(local: Path | None) -> bytes:
    """Загружает OpenAPI с портала или из файла для локальной проверки."""
    if local is not None:
        return local.read_bytes()
    with urlopen(SOURCE, timeout=30) as response:
        return response.read()


def main() -> None:
    """Генерирует SDK и при необходимости сверяет версии файлов без записи."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, help="Локальная копия опубликованной схемы OpenAPI (YAML или JSON)")
    parser.add_argument("--check", action="store_true", help="Сверить файлы с результатом генерации")
    args = parser.parse_args()
    raw_spec = _read_source(args.spec)
    spec = cast(Schema, yaml.safe_load(raw_spec))
    names = cast(dict[str, dict[str, str]], yaml.safe_load(OPERATIONS.read_text(encoding="utf-8")))

    # Собираем оба файла во временном каталоге и заменяем их только после успешной генерации.
    with TemporaryDirectory(prefix="mindvoice-sdk-") as temp_dir:
        temporary = Path(temp_dir)
        source = temporary / "openapi.json"
        # Порядок ключей в YAML портала и выгрузке JSON не влияет на модели.
        source.write_text(json.dumps(spec, sort_keys=True, ensure_ascii=False), encoding="utf-8")
        operations_file, models_file = temporary / "_operations.py", temporary / "models.py"
        operations_file.write_text(_render_operations(spec, names), encoding="utf-8")
        _generate_models(source, models_file)
        for command in (["check", "--fix", "--select", "I,UP029", "--unsafe-fixes"], ["format"]):
            subprocess.run(
                [sys.executable, "-m", "ruff", *command, "--config", str(ROOT / "pyproject.toml"), str(operations_file), str(models_file)],
                check=True,
            )
        for generated in (operations_file, models_file):
            target = ROOT / OUTPUT / generated.name
            if args.check:
                if not target.is_file() or target.read_bytes() != generated.read_bytes():
                    raise SystemExit(f"Обновите сгенерированный файл {target.relative_to(ROOT)}")
            else:
                target.write_bytes(generated.read_bytes())


if __name__ == "__main__":
    main()
