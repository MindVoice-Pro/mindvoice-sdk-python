# Сгенерировано из OpenAPI MindVoice командой uv run python scripts/generate.py.

from __future__ import annotations

from datetime import date
from typing import Annotated, Any, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, JsonValue
from typing_extensions import TypeAliasType


class ActivationRequest(BaseModel):
    """
    Запрос изменения активности сценария.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    active: Annotated[bool, Field(title="Active")]
    """
    Активность.
    """


class AnalysisCriterionGroup(BaseModel):
    """
    Группа одного сценария; код сохраняется при перестановке и клонировании.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    code: Annotated[str, Field(pattern="^[a-z][a-z0-9_]{0,63}$", title="Code")]
    id: Annotated[str, Field(min_length=1, title="Id")]
    title: Annotated[str, Field(min_length=1, title="Title")]
    weight: Annotated[int | None, Field(ge=1, title="Weight")] = None
    """
    Порядковый номер группы, не коэффициент оценки.
    """


class AnalysisResultItemSource(BaseModel):
    """
    Источник данных для AnalysisResultItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    analysis_run_id: Annotated[
        str,
        Field(
            pattern="^anl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Analysis Run Id",
        ),
    ]
    """
    Идентификатор запуска анализа.
    """
    analysis_scenario_id: Annotated[
        str,
        Field(
            pattern="^sca-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Analysis Scenario Id",
        ),
    ]
    """
    Идентификатор сценария анализа.
    """
    recording_id: Annotated[
        str,
        Field(
            pattern="^fl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Recording Id",
        ),
    ]
    """
    Идентификатор аудиозаписи.
    """
    transcription_run_id: Annotated[
        str,
        Field(
            pattern="^trn-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Transcription Run Id",
        ),
    ]
    """
    Идентификатор запуска транскрибации.
    """


class AnalysisResultItemStatistics(BaseModel):
    """
    Счётчики результата анализа по историческим правилам критериев.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    critical_count: Annotated[int, Field(ge=0, le=4294967295, title="Critical Count")]
    """
    Количество критериев с is_critical=true; один критерий даёт не более одного отклонения.
    """


class AnalysisRunCreate(BaseModel):
    """
    Запрос запуска анализа с необязательным выбором конкретного transcript.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    analysis_scenario_id: Annotated[
        str,
        Field(
            pattern="^sca-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Analysis Scenario Id",
        ),
    ]
    """
    Идентификатор сценария анализа.
    """
    transcript_id: Annotated[str | None, Field(title="Transcript Id")] = None
    """
    Идентификатор текста расшифровки.
    """


class AnalysisRunDetailError(BaseModel):
    """
    Сведения об ошибке для AnalysisRunDetail.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    code: Annotated[str | None, Field(title="Code")] = None
    """
    Стабильный доменный код ошибки.
    """
    message: Annotated[str | None, Field(title="Message")] = None
    """
    Безопасное пояснение ошибки.
    """


class AnalysisRunDetailModel(BaseModel):
    """
    Выбранная модель для AnalysisRunDetail.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    analysis_scenario_id: Annotated[
        str,
        Field(
            pattern="^sca-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Analysis Scenario Id",
        ),
    ]
    """
    Идентификатор сценария анализа.
    """
    analysis_scenario_version: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Analysis Scenario Version")]
    """
    Версия неизменного сценария анализа.
    """
    display_name: Annotated[str, Field(title="Display Name")]
    """
    Модель либо фильтр моделей согласно типу поля.
    """
    provider: Annotated[str, Field(title="Provider")]
    """
    Код провайдера.
    """
    scenario_name: Annotated[str, Field(title="Scenario Name")]
    """
    Название сценария.
    """
    snapshot_id: Annotated[
        str,
        Field(
            pattern="^anl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Snapshot Id",
        ),
    ]
    """
    Идентификатор неизменного снимка анализа.
    """


class AnalysisRunDetailStatistics(BaseModel):
    """
    Сводные показатели для AnalysisRunDetail.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    flags_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Flags Count")]
    """
    Число критериев с отклонениями.
    """
    questions_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Questions Count")]
    """
    Количество критериев.
    """


class AnalysisRunItemError(BaseModel):
    """
    Сведения об ошибке для AnalysisRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    code: Annotated[str | None, Field(title="Code")] = None
    """
    Стабильный доменный код ошибки.
    """
    message: Annotated[str | None, Field(title="Message")] = None
    """
    Безопасное пояснение ошибки.
    """


class AnalysisRunItemModel(BaseModel):
    """
    Выбранная модель для AnalysisRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    analysis_scenario_id: Annotated[
        str,
        Field(
            pattern="^sca-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Analysis Scenario Id",
        ),
    ]
    """
    Идентификатор сценария анализа.
    """
    analysis_scenario_version: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Analysis Scenario Version")]
    """
    Версия неизменного сценария анализа.
    """


class AnalysisScenarioExecutionCreate(BaseModel):
    """
    Запрос пакетного запуска сценария анализа.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    idempotency_key: Annotated[str | None, Field(max_length=255, title="Idempotency Key")] = None
    """
    Ключ повторяемой операции в прежней области уникальности; повтор не создаёт новое выполнение.
    """
    recording_ids: Annotated[list[str] | None, Field(title="Recording Ids")] = None
    """
    Явно выбранные записи; отсутствие означает отбор по сценарию.
    """


class AnalysisScenarioExecutionItemStatistics(BaseModel):
    """
    Сводные показатели для app__analysis__schemas__ScenarioExecutionItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    completed_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Completed Count")]
    """
    Количество успешно завершённых элементов.
    """
    duration_seconds: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Duration Seconds")]
    """
    Длительность, секунды.
    """
    failed_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Failed Count")]
    """
    Число ошибочных элементов.
    """
    preparation_processed_count: Annotated[int | None, Field(ge=0, le=2147483647, title="Preparation Processed Count")] = 0
    """
    Число проверенных файлов снимка, включая пропущенные.
    """
    preparation_skipped_count: Annotated[int | None, Field(ge=0, le=2147483647, title="Preparation Skipped Count")] = 0
    """
    Число файлов, ставших недоступными для запуска во время подготовки.
    """
    preparation_total_count: Annotated[int | None, Field(ge=0, le=2147483647, title="Preparation Total Count")] = None
    """
    Размер снимка файлов; поле отсутствует до завершения отбора.
    """
    processing_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Processing Count")]
    """
    Число элементов в обработке.
    """
    queued_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Queued Count")]
    """
    Число элементов в очереди.
    """
    total_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Total Count")]
    """
    Количество элементов выборки.
    """


class AnalysisSummaryModelSettings(BaseModel):
    """
    Параметры сэмплирования сводки AI-анализа.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    temperature: Annotated[float | None, Field(ge=0.0, le=1.0, title="Temperature")] = None
    """
    Температура сводки, по умолчанию 0.3 для новой формы.
    """
    top_p: Annotated[float | None, Field(ge=0.0, le=1.0, title="Top P")] = None
    """
    Top P сводки, по умолчанию 0.8 для новой формы.
    """


class AudioQuality(BaseModel):
    """
    Типизированное сообщение AudioQuality.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    average_loudness_lufs: Annotated[float | None, Field(title="Average Loudness Lufs")] = None
    """
    Средняя громкость LUFS.
    """
    clipped_samples_ratio: Annotated[float | None, Field(ge=0.0, le=1.0, title="Clipped Samples Ratio")] = None
    """
    Доля клиппированных отсчётов от 0 до 1.
    """
    has_clipping: Annotated[bool | None, Field(title="Has Clipping")] = None
    """
    Есть цифровой клиппинг.
    """
    peak_dbfs: Annotated[float | None, Field(title="Peak Dbfs")] = None
    """
    Пиковый уровень dBFS.
    """
    silence_seconds: Annotated[float | None, Field(ge=0.0, title="Silence Seconds")] = None
    """
    Суммарная тишина, секунды.
    """
    warning: Annotated[str | None, Field(title="Warning")] = None
    """
    Предупреждение о качестве.
    """


DateBoundary1 = TypeAliasType(
    "DateBoundary1",
    Annotated[
        Any,
        Field(examples=["2026-09-30", "2026-09-30T10:00:00Z"], title="DateBoundary"),
    ],
)
"""
Граница фильтра: календарная дата YYYY-MM-DD либо момент RFC 3339. Смысл календарной верхней границы описан для конкретного фильтра; это string в protobuf, а не Timestamp.
"""


DecimalValue = TypeAliasType(
    "DecimalValue",
    Annotated[
        str,
        Field(
            examples=["0.07851"],
            pattern="^-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?$",
            title="DecimalValue",
        ),
    ],
)
"""
Точное десятичное число без экспоненты; protobuf string с Decimal-валидацией.
"""


class FieldViolation(BaseModel):
    """
    Типизированное сообщение FieldViolation.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    code: Annotated[str, Field(title="Code")]
    """
    Машинный код нарушения.
    """
    field_path: Annotated[str, Field(title="Field Path")]
    """
    Путь поля в snake_case, индексы массива через точку.
    """
    message: Annotated[str, Field(title="Message")]
    """
    Объяснение на русском языке.
    """


IntegerMap = TypeAliasType("IntegerMap", dict[str, int])
"""
Словарь счётчиков, protobuf map<string, int32>.
"""


class MetadataFilter(BaseModel):
    """
    Типизированное сообщение MetadataFilter.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    field: Annotated[str, Field(title="Field")]
    """
    Ключ пользовательских метаданных.
    """
    include_empty: Annotated[bool | None, Field(title="Include Empty")] = None
    """
    Включать отсутствующие, null и пустые строки; только для in/not_in.
    """
    operator: Annotated[
        Literal[
            "equals",
            "not_equals",
            "contains",
            "exists",
            "in",
            "not_in",
            "date_from",
            "date_to",
            "num_from",
            "num_to",
        ],
        Field(title="Operator"),
    ]
    """
    Оператор сравнения.
    """
    value: JsonValue | None = None
    """
    Значение сравнения; тип проверяется в зависимости от operator.
    """


class MetadataGroup(BaseModel):
    """
    Группа условий метаданных; максимум 5 уровней, 100 условий и 200 узлов.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    conditions: Annotated[
        list[MetadataFilter | MetadataGroup],
        Field(max_length=200, min_length=1, title="Conditions"),
    ]
    logic: Annotated[Literal["and", "or"] | None, Field(title="Logic")] = "and"


class Pagination(BaseModel):
    """
    Метаданные страницы. Возможности пагинации конкретного пути не расширяются автоматически.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    offset: Annotated[int | None, Field(ge=0, le=2147483647, title="Offset")] = None
    """
    Смещение страницы в отфильтрованной выборке.
    """
    page_size: Annotated[int, Field(ge=0, le=2147483647, title="Page Size")]
    """
    Запрошенный размер страницы; 0 только там, где текущий API разрешает его.
    """
    total_count: Annotated[int | None, Field(ge=0, le=4294967295, title="Total Count")] = None
    """
    Количество всей отфильтрованной выборки, а не страницы; целое число uint32.
    """


class QuestionOption(BaseModel):
    """
    Типизированное сообщение QuestionOption.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    is_critical: Annotated[bool | None, Field(title="Is Critical")] = False
    """
    Вариант отмечен как отклонение в историческом определении критерия.
    """
    key: Annotated[str, Field(title="Key")]
    """
    Уникальный ключ варианта.
    """
    label: Annotated[str, Field(title="Label")]
    """
    Название варианта.
    """


class RecordingFilter(BaseModel):
    """
    Типизированное сообщение RecordingFilter.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    dedup_policy: Annotated[str | None, Field(title="Dedup Policy")] = None
    """
    Политика отбора уже обработанных файлов; действующие значения сохраняются.
    """
    duration_from: Annotated[int | None, Field(ge=0, le=2147483647, title="Duration From")] = None
    """
    Минимум длительности, секунды.
    """
    duration_to: Annotated[int | None, Field(ge=0, le=2147483647, title="Duration To")] = None
    """
    Максимум длительности, секунды.
    """
    file_id: Annotated[str | None, Field(title="File Id")] = None
    """
    Идентификатор записи.
    """
    metadata_filters: Annotated[list[MetadataFilter] | None, Field(title="Metadata Filters")] = None
    """
    Условия сравнения метаданных.
    """
    metadata_group: MetadataGroup | None = None
    """
    Дерево условий И/ИЛИ; не совмещается с непустым metadata_filters.
    """
    metadata_logic: Annotated[Literal["and", "or"] | None, Field(title="Metadata Logic")] = None
    """
    Связь плоских условий метаданных; по умолчанию И.
    """
    only_without_transcription: Annotated[bool | None, Field(title="Only Without Transcription")] = None
    """
    Только записи без текста расшифровки.
    """
    search: Annotated[str | None, Field(title="Search")] = None
    """
    Поиск имени записи.
    """
    silence_ratio_from: Annotated[float | None, Field(ge=0.0, le=100.0, title="Silence Ratio From")] = None
    """
    Минимальная доля тишины, проценты.
    """
    silence_ratio_to: Annotated[float | None, Field(ge=0.0, le=100.0, title="Silence Ratio To")] = None
    """
    Максимальная доля тишины, проценты.
    """
    size_from: Annotated[float | None, Field(ge=0.0, title="Size From")] = None
    """
    Минимум размера, МиБ.
    """
    size_to: Annotated[float | None, Field(ge=0.0, title="Size To")] = None
    """
    Максимум размера, МиБ.
    """
    source: Annotated[list[str] | None, Field(title="Source")] = None
    """
    Источники загрузки.
    """
    status: Annotated[list[str] | None, Field(title="Status")] = None
    """
    Допустимые состояния.
    """
    uploaded_from: str | None = None
    """
    Нижняя граница даты загрузки.
    """
    uploaded_to: str | None = None
    """
    Верхняя граница загрузки; календарная дата включает весь день.
    """


class RecordingImportFile(BaseModel):
    """
    Свойства файла для RecordingImport.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    filename: Annotated[str | None, Field(max_length=512, min_length=1, title="Filename")] = None
    """
    Имя файла.
    """
    url: Annotated[str, Field(max_length=8192, min_length=1, title="Url")]
    """
    URL или HTTP-путь согласно формату поля.
    """


class RecordingImportRetry(BaseModel):
    """
    Запрос повторного импорта с необязательной заменой истёкшей ссылки.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    check_duplicates: Annotated[bool | None, Field(title="Check Duplicates")] = None
    """
    Меняет проверку дублей для повторного импорта; отсутствие сохраняет прежний выбор.
    """
    url: Annotated[str | None, Field(max_length=8192, min_length=1, title="Url")] = None
    """
    URL или HTTP-путь согласно формату поля.
    """


class RecordingImportStorage(BaseModel):
    """
    Хранение и срок удаления для RecordingImport.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    retention_days: Annotated[int | None, Field(ge=1, le=2147483647, title="Retention Days")] = None
    """
    Срок хранения, дни.
    """


class RecordingItemStatistics(BaseModel):
    """
    Сводные показатели для RecordingItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    analyses_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Analyses Count")]
    """
    Число успешно завершённых нетестовых запусков анализа записи.
    """
    transcriptions_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Transcriptions Count")]
    """
    Число текстов расшифровки записи.
    """


class RecordingUpdateFile(BaseModel):
    """
    Свойства файла для RecordingUpdate.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    filename: Annotated[str | None, Field(max_length=512, min_length=1, title="Filename")] = None
    """
    Имя файла.
    """


class RunStatistics(BaseModel):
    """
    Типизированное сообщение RunStatistics.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    status_counts: IntegerMap
    """
    Число запусков каждого состояния во всей отфильтрованной выборке.
    """


class ScenarioSchedule(BaseModel):
    """
    Типизированное сообщение ScenarioSchedule.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    frequency: Annotated[Literal["hourly", "daily", "weekly"], Field(title="Frequency")]
    """
    Частота.
    """
    time: Annotated[str | None, Field(pattern="^(?:[01][0-9]|2[0-3]):[0-5][0-9]$", title="Time")] = None
    """
    Локальное время.
    """
    timezone: Annotated[str, Field(title="Timezone")]
    """
    Часовой пояс IANA, проверяется сервером.
    """
    weekday: Annotated[int | None, Field(ge=0, le=6, title="Weekday")] = None
    """
    День недели: понедельник=0, воскресенье=6.
    """


class SelectedOption(BaseModel):
    """
    Выбранный вариант ответа из исторического снимка сценария.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    is_critical: Annotated[bool | None, Field(title="Is Critical")] = False
    """
    Вариант отмечен как отклонение в историческом определении критерия.
    """
    key: Annotated[str, Field(title="Key")]
    """
    Код выбранного варианта.
    """
    label: Annotated[str | None, Field(title="Label")] = None
    """
    Историческое название; отсутствует, если его невозможно восстановить.
    """


class SelectedOptions(BaseModel):
    """
    Выбранные варианты в порядке ответа модели, включая пустой выбор.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    options: Annotated[list[SelectedOption], Field(title="Options")]
    """
    Выбранные варианты; пустой массив означает отсутствие выбора.
    """


StringMap = TypeAliasType("StringMap", dict[str, str])
"""
Словарь строк, protobuf map<string, string>.
"""


class SummaryDetail(BaseModel):
    """
    Типизированное сообщение SummaryDetail.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    key_events: Annotated[list[str], Field(title="Key Events")]
    """
    Ключевые события; исходное поле keyEvents.
    """
    overview: Annotated[str, Field(min_length=1, title="Overview")]
    """
    Обзор разговора.
    """
    problems: Annotated[list[str], Field(title="Problems")]
    """
    Обнаруженные проблемы.
    """
    topics: Annotated[list[str], Field(title="Topics")]
    """
    Темы разговора.
    """


class TextStatistics(BaseModel):
    """
    Типизированное сообщение TextStatistics.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    characters_with_spaces: Annotated[int, Field(ge=0, le=2147483647, title="Characters With Spaces")]
    """
    Количество символов с пробелами.
    """
    characters_without_spaces: Annotated[int, Field(ge=0, le=2147483647, title="Characters Without Spaces")]
    """
    Количество символов без пробелов.
    """
    word_count: Annotated[int, Field(ge=0, le=2147483647, title="Word Count")]
    """
    Количество слов.
    """


class TimeRange(BaseModel):
    """
    Типизированное сообщение TimeRange.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    end_seconds: Annotated[float, Field(ge=0.0, title="End Seconds")]
    """
    Конец относительно начала аудиозаписи, секунды; не меньше начала.
    """
    start_seconds: Annotated[float, Field(ge=0.0, title="Start Seconds")]
    """
    Начало относительно начала аудиозаписи, секунды.
    """


Timestamp = TypeAliasType(
    "Timestamp",
    Annotated[AwareDatetime, Field(examples=["2026-09-30T10:00:00Z"], title="Timestamp")],
)
"""
Момент времени RFC 3339; ответы нормализованы в UTC, protobuf Timestamp.
"""


class TokenCostBreakdown(BaseModel):
    """
    Раздельные точные стоимости входных и выходных токенов.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    currency: Annotated[str | None, Field(title="Currency")] = None
    """
    Валюта расчёта.
    """
    input_cost: DecimalValue | None = None
    """
    Стоимость входных токенов после тарификации.
    """
    output_cost: DecimalValue | None = None
    """
    Стоимость выходных токенов после тарификации.
    """


class TranscriptSearchHit(BaseModel):
    """
    Типизированное сообщение TranscriptSearchHit.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    confidence: Annotated[float, Field(ge=0.0, le=1.0, title="Confidence")]
    """
    Уверенность поиска.
    """
    snippet: Annotated[str, Field(title="Snippet")]
    """
    Фрагмент текста совпадения.
    """
    time_range: TimeRange
    """
    Смещения в исходном аудио, секунды.
    """


class TranscriptSearchResult(BaseModel):
    """
    Результат одного поискового запроса в аудиоканале, включая отсутствие совпадений.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    channel: Annotated[int, Field(ge=0, le=2147483647, title="Channel")]
    """
    Канал аудио или realtime-подписки; конкретный тип определяется схемой.
    """
    hits: Annotated[list[TranscriptSearchHit] | None, Field(title="Hits")] = None
    """
    Совпадения поискового запроса.
    """
    query: Annotated[str, Field(title="Query")]
    """
    Поисковая строка.
    """


class TranscriptSegment(BaseModel):
    """
    Типизированное сообщение TranscriptSegment.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    absolute_time_range: TimeRange
    """
    Абсолютные смещения в исходном аудио после нарезки на части.
    """
    confidence: Annotated[float | None, Field(ge=0.0, le=1.0, title="Confidence")] = None
    """
    Оценка уверенности провайдера; отсутствие не равно нулю.
    """
    speaker_id: Annotated[str | None, Field(title="Speaker Id")] = None
    """
    Идентификатор говорящего, без предположения о его личности.
    """
    text: Annotated[str, Field(title="Text")]
    """
    Текст сегмента.
    """
    time_range: TimeRange
    """
    Смещения в исходном аудио, секунды.
    """


class TranscriptSummary(BaseModel):
    """
    Типизированное сообщение TranscriptSummary.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    detail: SummaryDetail | None = None
    """
    Структурированное резюме; отсутствует до получения результата.
    """
    status: Annotated[Literal["none", "processing", "ready", "failed"], Field(title="Status")]
    """
    Состояние независимой генерации резюме.
    """
    text: Annotated[str | None, Field(title="Text")] = None
    """
    Краткое резюме; отсутствует до получения результата.
    """


class TranscriptWord(BaseModel):
    """
    Типизированное сообщение TranscriptWord.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    absolute_time_range: TimeRange
    """
    Абсолютные смещения в исходном аудио после нарезки на части.
    """
    confidence: Annotated[float | None, Field(ge=0.0, le=1.0, title="Confidence")] = None
    """
    Оценка уверенности провайдера; отсутствие не равно нулю.
    """
    speaker_id: Annotated[str | None, Field(title="Speaker Id")] = None
    """
    Идентификатор говорящего, без предположения о его личности.
    """
    text: Annotated[str, Field(title="Text")]
    """
    Слово с пунктуацией, если её возвращает провайдер.
    """
    time_range: TimeRange
    """
    Смещения в исходном аудио, секунды.
    """


class TranscriptionRunCreate(BaseModel):
    """
    Запрос запуска транскрибации.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    transcription_scenario_id: Annotated[
        str,
        Field(
            pattern="^sct-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Transcription Scenario Id",
        ),
    ]
    """
    Идентификатор сценария распознавания.
    """


class TranscriptionRunItemBilling(BaseModel):
    """
    Сохранённая стоимость транскрибации до скидок.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cost: Annotated[str, Field(pattern="^-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?$", title="Cost")]
    """
    Полная сохранённая стоимость STT в рублях до скидок и грантов, без отдельного LLM-резюме.
    """


class TranscriptionRunItemError(BaseModel):
    """
    Сведения об ошибке для TranscriptionRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    code: Annotated[str | None, Field(title="Code")] = None
    """
    Стабильный доменный код ошибки.
    """
    message: Annotated[str | None, Field(title="Message")] = None
    """
    Безопасное пояснение ошибки.
    """
    reason: Annotated[
        Literal[
            "timeout",
            "service_unavailable",
            "rate_limited",
            "invalid_audio",
            "access_denied",
            "invalid_response",
            "unknown",
        ]
        | None,
        Field(title="Reason"),
    ] = None
    """
    Безопасная категория причины ошибки транскрибации; старые ошибки могут её не иметь.
    """


class TranscriptionRunItemExecution(BaseModel):
    """
    Параметры выполнения для TranscriptionRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cancelled_at: Timestamp | None = None
    """
    Дата отмены.
    """
    cancelled_by: Annotated[str | None, Field(title="Cancelled By")] = None
    """
    Идентификатор отменившего пользователя.
    """
    created_at: Timestamp
    """
    Дата создания.
    """
    failed_at: Timestamp | None = None
    """
    Дата ошибки обработки.
    """
    finished_at: Timestamp | None = None
    """
    Дата окончания выполнения.
    """
    job_id: Annotated[str | None, Field(title="Job Id")] = None
    """
    Идентификатор пакетного выполнения.
    """
    started_at: Timestamp | None = None
    """
    Начало выполнения.
    """
    status: Annotated[
        Literal["queued", "processing", "completed", "failed", "cancelled"],
        Field(title="Status"),
    ]
    """
    Состояние ресурса.
    """
    worker: Annotated[str | None, Field(title="Worker")] = None
    """
    Безопасный технический идентификатор обработчика.
    """


class TranscriptionRunItemModel(BaseModel):
    """
    Выбранная модель для TranscriptionRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    display_name: Annotated[str | None, Field(title="Display Name")] = None
    """
    Модель либо фильтр моделей согласно типу поля.
    """
    scenario_name: Annotated[str | None, Field(title="Scenario Name")] = None
    """
    Название сценария.
    """
    transcription_scenario_id: Annotated[
        str,
        Field(
            pattern="^sct-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Transcription Scenario Id",
        ),
    ]
    """
    Идентификатор сценария распознавания.
    """


class TranscriptionRunItemResult(BaseModel):
    """
    Результат выполнения для TranscriptionRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    has_diarization: Annotated[bool | None, Field(title="Has Diarization")] = False
    """
    В сегментах или словах результата есть непустые метки дикторов, включая ID 0.
    """
    has_summary: Annotated[bool | None, Field(title="Has Summary")] = False
    """
    Резюме уже сформировано.
    """
    is_annulled: Annotated[bool | None, Field(title="Is Annulled")] = False
    """
    Транскрибация необратимо аннулирована, включая неудачный запуск без текста.
    """
    summary_status: Annotated[str | None, Field(title="Summary Status")] = "none"
    """
    Состояние генерации резюме.
    """


class TranscriptionRunItemRetry(BaseModel):
    """
    Повторы обработки для TranscriptionRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    attempt_count: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Attempt Count")] = 0
    """
    Число выполненных попыток.
    """
    max_attempts: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Max Attempts")] = 1
    """
    Предельное число попыток.
    """
    next_attempt_at: Timestamp | None = None
    """
    Следующая попытка.
    """
    retry_count: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Retry Count")] = 0
    """
    Количество ручных повторов.
    """
    retry_of_id: Annotated[
        str | None,
        Field(
            pattern="^trn-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Retry Of Id",
        ),
    ] = None
    """
    Исходный запуск при повторе.
    """
    retryable: Annotated[bool | None, Field(title="Retryable")] = False
    """
    Разрешён ручной повтор ошибки, включая provider_result_unknown, если исходный файл доступен и преемник ещё не создан.
    """


class TranscriptionRunItemStatistics(BaseModel):
    """
    Сводные показатели для TranscriptionRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    analyses_count: Annotated[int | None, Field(ge=0, le=2147483647, title="Analyses Count")] = 0
    """
    Число успешно завершённых нетестовых анализов конкретной транскрибации.
    """
    characters_with_spaces: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Characters With Spaces")] = 0
    """
    Символы с пробелами.
    """
    characters_without_spaces: Annotated[
        int | None,
        Field(ge=-2147483648, le=2147483647, title="Characters Without Spaces"),
    ] = 0
    """
    Символы без пробелов.
    """
    word_count: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Word Count")] = 0
    """
    Количество слов.
    """


class TranscriptionScenarioExecutionCreate(BaseModel):
    """
    Запрос пакетного запуска сценария транскрибации.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    idempotency_key: Annotated[str | None, Field(max_length=255, title="Idempotency Key")] = None
    """
    Ключ повторяемой операции в прежней области уникальности; повтор не создаёт новое выполнение.
    """
    recording_ids: Annotated[list[str] | None, Field(title="Recording Ids")] = None
    """
    Явно выбранные записи; отсутствие означает отбор по сценарию.
    """


class TranscriptionScenarioExecutionItemExecution(BaseModel):
    """
    Параметры выполнения для app__transcription__schemas__ScenarioExecutionItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    created_at: Timestamp
    """
    Дата создания.
    """
    finished_at: Timestamp | None = None
    """
    Дата окончания выполнения.
    """
    preparation_error_code: Annotated[str | None, Field(title="Preparation Error Code")] = None
    """
    Безопасный код ошибки подготовки пакета.
    """
    preparation_status: Annotated[
        Literal["pending", "preparing", "completed", "failed"] | None,
        Field(title="Preparation Status"),
    ] = "completed"
    """
    Этап подготовки пакета: ожидание, отбор и создание задач, завершение либо ошибка.
    """
    started_at: Timestamp | None = None
    """
    Начало выполнения.
    """
    status: Annotated[str, Field(title="Status")]
    """
    Состояние ресурса.
    """


class TranscriptionScenarioExecutionItemStatistics(BaseModel):
    """
    Сводные показатели для app__transcription__schemas__ScenarioExecutionItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    completed_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Completed Count")]
    """
    Количество успешно завершённых элементов.
    """
    duration_seconds: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Duration Seconds")]
    """
    Длительность, секунды.
    """
    failed_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Failed Count")]
    """
    Число ошибочных элементов.
    """
    preparation_processed_count: Annotated[int | None, Field(ge=0, le=2147483647, title="Preparation Processed Count")] = 0
    """
    Число проверенных файлов снимка, включая пропущенные.
    """
    preparation_skipped_count: Annotated[int | None, Field(ge=0, le=2147483647, title="Preparation Skipped Count")] = 0
    """
    Число файлов, ставших недоступными для запуска во время подготовки.
    """
    preparation_total_count: Annotated[int | None, Field(ge=0, le=2147483647, title="Preparation Total Count")] = None
    """
    Размер снимка файлов; поле отсутствует до завершения отбора.
    """
    processed_duration_seconds: Annotated[int | None, Field(ge=0, le=9007199254740991, title="Processed Duration Seconds")] = None
    """
    Обработанная длительность, секунды.
    """
    processing_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Processing Count")]
    """
    Число элементов в обработке.
    """
    queued_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Queued Count")]
    """
    Число элементов в очереди.
    """
    total_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Total Count")]
    """
    Количество элементов выборки.
    """


class TranscriptionScenarioItemAudit(BaseModel):
    """
    Сведения о создании и изменении для TranscriptionScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cloned_from_id: Annotated[
        str | None,
        Field(
            pattern="^sct-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Cloned From Id",
        ),
    ] = None
    """
    Исходный сценарий клонирования.
    """
    created_at: Timestamp
    """
    Дата создания.
    """
    created_by: Annotated[str | None, Field(title="Created By")] = None
    """
    Автор создания.
    """
    updated_at: Timestamp
    """
    Дата последнего изменения.
    """


class TranscriptionScenarioItemStatistics(BaseModel):
    """
    Сводные показатели для TranscriptionScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    failed_runs: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Failed Runs")]
    """
    Число неуспешных запусков.
    """
    last_run_at: Timestamp | None = None
    """
    Последний запуск.
    """
    runs: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Runs")]
    """
    Число запусков.
    """
    success_runs: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Success Runs")]
    """
    Успешные запуски.
    """


class TranscriptionScenarioItemTrigger(BaseModel):
    """
    Условия запуска для TranscriptionScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    file_filter: RecordingFilter
    """
    Условия отбора аудиозаписей.
    """
    schedule: ScenarioSchedule | None = None
    """
    Расписание, формат определяется схемой.
    """
    trigger_type: Annotated[Literal["manual", "auto", "scheduled"], Field(title="Trigger Type")]
    """
    Способ запуска сценария.
    """


UInt64Value = TypeAliasType(
    "UInt64Value",
    Annotated[
        str,
        Field(
            examples=["8421120"],
            pattern="^(?:0|[1-9][0-9]{0,19})$",
            title="UInt64Value",
        ),
    ],
)
"""
Неотрицательный uint64 в десятичной строке без потери точности JavaScript.
"""


class WorkspaceBalance(BaseModel):
    """
    Типизированное сообщение WorkspaceBalance.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    amount: DecimalValue | None = None
    """
    Точная сумма.
    """
    available_amount: DecimalValue | None = None
    """
    Доступная сумма после резервирования.
    """
    currency: Annotated[str | None, Field(title="Currency")] = None
    """
    Валюта счёта.
    """
    reserved_amount: DecimalValue | None = None
    """
    Зарезервированная точная сумма.
    """


class WorkspaceItemAccess(BaseModel):
    """
    Права и доступность для WorkspaceItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    can_view_finances: Annotated[bool | None, Field(title="Can View Finances")] = False
    """
    Разрешён просмотр финансов.
    """
    is_default: Annotated[bool, Field(title="Is Default")]
    """
    Ресурс выбран по умолчанию.
    """
    role: Annotated[str, Field(title="Role")]
    """
    Роль участника в указанном контексте.
    """


class WorkspaceItemAudit(BaseModel):
    """
    Сведения о создании и изменении для WorkspaceItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    created_at: Timestamp
    """
    Дата создания.
    """


class WorkspaceOverviewPlan(BaseModel):
    """
    Тариф и период текущего обзора Workspace.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    is_public: Annotated[bool, Field(title="Is Public")]
    """
    Публичный тариф.
    """
    name: Annotated[str, Field(title="Name")]
    """
    Название текущего тарифа.
    """
    period_end: Annotated[date, Field(title="Period End")]
    """
    Текущая дата периода по Москве.
    """
    period_start: Annotated[date, Field(title="Period Start")]
    """
    Начальная дата текущего периода.
    """
    retention_days: Annotated[int | None, Field(ge=0, title="Retention Days")] = None
    """
    Срок хранения, дни.
    """
    retention_hours: Annotated[int | None, Field(ge=0, title="Retention Hours")] = None
    """
    Срок хранения, часы.
    """


class WorkspaceOverviewStatistics(BaseModel):
    """
    Сводные показатели для WorkspaceOverview.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    completed_transcriptions_count: Annotated[
        int | None,
        Field(ge=-2147483648, le=2147483647, title="Completed Transcriptions Count"),
    ] = 0
    """
    Число завершённых транскрибаций.
    """
    files_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Files Count")]
    """
    Число исходников.
    """
    processing_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Processing Count")]
    """
    Число элементов в обработке.
    """
    storage_bytes: UInt64Value | None = None
    """
    Объём хранения, байты.
    """
    transcription_seconds: Annotated[float | None, Field(title="Transcription Seconds")] = 0
    """
    Обработанная длительность, секунды.
    """


class AnalysisQuestion(BaseModel):
    """
    Типизированное сообщение AnalysisQuestion.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    additional_prompt: Annotated[str | None, Field(title="Additional Prompt")] = None
    """
    Необязательный промпт этого определения критерия; пустое значение эквивалентно отсутствию.
    """
    allow_no_answer: Annotated[bool | None, Field(title="Allow No Answer")] = True
    """
    Допустим пустой выбор.
    """
    analytics_action: Annotated[Literal["same", "new"] | None, Field(title="Analytics Action")] = None
    """
    Решение при изменении вопроса: объединить или создать отдельный критерий; только запрос.
    """
    criterion_code: Annotated[
        str,
        Field(max_length=64, pattern="^[a-z][a-z0-9_]{0,63}$", title="Criterion Code"),
    ]
    """
    Код критерия на момент сохранения конфигурации.
    """
    criterion_id: Annotated[
        str,
        Field(
            pattern="^(crit-)?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Criterion Id",
        ),
    ]
    """
    Постоянный идентификатор критерия Workspace в формате crit-UUID.
    """
    criterion_version: Annotated[int, Field(ge=1, title="Criterion Version")]
    """
    Неизменяемая версия определения критерия.
    """
    flag_when: Annotated[bool | None, Field(title="Flag When")] = None
    """
    Значение булевого ответа, означающее отклонение.
    """
    group_id: Annotated[str | None, Field(title="Group Id")] = None
    """
    ID группы в этом сценарии; null для критерия без группы.
    """
    id: Annotated[str | None, Field(title="Id")] = None
    """
    Прежнее поле идентификатора критерия; при сохранении совпадает с criterion_id в формате crit-UUID.
    """
    options: Annotated[list[QuestionOption] | None, Field(title="Options")] = None
    """
    Варианты списочного критерия; ключи уникальны.
    """
    prompt: Annotated[str, Field(min_length=1, title="Prompt")]
    """
    Инструкция модели.
    """
    required: Annotated[bool | None, Field(title="Required")] = True
    """
    Обязательность ответа.
    """
    selection_mode: Annotated[Literal["single", "multiple"] | None, Field(title="Selection Mode")] = "single"
    """
    Режим выбора.
    """
    severity: Annotated[Literal["none", "low", "medium", "high"] | None, Field(title="Severity")] = "none"
    """
    Важность отклонения.
    """
    title: Annotated[str, Field(min_length=1, title="Title")]
    """
    Название критерия.
    """
    type: Annotated[Literal["boolean", "text", "list"], Field(title="Type")]
    """
    Тип критерия.
    """
    weight: Annotated[int | None, Field(ge=1, title="Weight")] = None
    """
    Сквозной порядковый номер 1..N, не коэффициент оценки.
    """


class AnalysisQuestionInput(BaseModel):
    """
    Новый или выбранный вопрос при создании сценария.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    additional_prompt: Annotated[str | None, Field(title="Additional Prompt")] = None
    """
    Необязательный промпт этого определения критерия; пустое значение эквивалентно отсутствию.
    """
    allow_no_answer: Annotated[bool | None, Field(title="Allow No Answer")] = True
    """
    Допустим пустой выбор.
    """
    analytics_action: Annotated[Literal["same", "new"] | None, Field(title="Analytics Action")] = None
    """
    Решение при изменении вопроса: объединить или создать отдельный критерий; только запрос.
    """
    criterion_code: Annotated[
        str | None,
        Field(max_length=64, pattern="^[a-z][a-z0-9_]{0,63}$", title="Criterion Code"),
    ] = None
    """
    Код критерия на момент сохранения конфигурации.
    """
    criterion_id: Annotated[
        str | None,
        Field(
            pattern="^(crit-)?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Criterion Id",
        ),
    ] = None
    """
    Постоянный идентификатор критерия Workspace в формате crit-UUID.
    """
    criterion_version: Annotated[int | None, Field(ge=1, title="Criterion Version")] = None
    """
    Неизменяемая версия определения критерия.
    """
    flag_when: Annotated[bool | None, Field(title="Flag When")] = None
    """
    Значение булевого ответа, означающее отклонение.
    """
    group_id: Annotated[str | None, Field(title="Group Id")] = None
    """
    ID группы в этом сценарии; null для критерия без группы.
    """
    id: Annotated[str | None, Field(title="Id")] = None
    """
    Прежнее поле идентификатора критерия; при сохранении совпадает с criterion_id в формате crit-UUID.
    """
    options: Annotated[list[QuestionOption] | None, Field(title="Options")] = None
    """
    Варианты списочного критерия; ключи уникальны.
    """
    prompt: Annotated[str, Field(min_length=1, title="Prompt")]
    """
    Инструкция модели.
    """
    required: Annotated[bool | None, Field(title="Required")] = True
    """
    Обязательность ответа.
    """
    selection_mode: Annotated[Literal["single", "multiple"] | None, Field(title="Selection Mode")] = "single"
    """
    Режим выбора.
    """
    severity: Annotated[Literal["none", "low", "medium", "high"] | None, Field(title="Severity")] = "none"
    """
    Важность отклонения.
    """
    title: Annotated[str, Field(min_length=1, title="Title")]
    """
    Название критерия.
    """
    type: Annotated[Literal["boolean", "text", "list"], Field(title="Type")]
    """
    Тип критерия.
    """
    weight: Annotated[int | None, Field(ge=1, title="Weight")] = None
    """
    Сквозной порядковый номер 1..N, не коэффициент оценки.
    """


class AnalysisRunDetailExecution(BaseModel):
    """
    Параметры выполнения для AnalysisRunDetail.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cancelled_at: Timestamp | None = None
    """
    Дата отмены.
    """
    cancelled_by: Annotated[str | None, Field(title="Cancelled By")] = None
    """
    Идентификатор отменившего пользователя.
    """
    created_at: Timestamp
    """
    Дата создания.
    """
    failed_at: Timestamp | None = None
    """
    Дата ошибки обработки.
    """
    finished_at: Timestamp | None = None
    """
    Дата окончания выполнения.
    """
    is_test: Annotated[bool | None, Field(title="Is Test")] = False
    """
    Платная проверка сценария.
    """
    processing_duration_sec: Annotated[
        int | None,
        Field(ge=-2147483648, le=2147483647, title="Processing Duration Sec"),
    ] = None
    """
    Длительность выполнения, секунды.
    """
    started_at: Timestamp | None = None
    """
    Начало выполнения.
    """
    status: Annotated[
        Literal["queued", "processing", "completed", "failed", "cancelled"],
        Field(title="Status"),
    ]
    """
    Состояние ресурса.
    """
    worker: Annotated[str | None, Field(title="Worker")] = None
    """
    Безопасный технический идентификатор обработчика.
    """


class AnalysisRunDetailRetry(BaseModel):
    """
    Повторы обработки для AnalysisRunDetail.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    attempt_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Attempt Count")]
    """
    Число выполненных попыток.
    """
    max_attempts: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Max Attempts")]
    """
    Предельное число попыток.
    """
    next_attempt_at: Timestamp | None = None
    """
    Следующая попытка.
    """
    retry_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Retry Count")]
    """
    Количество ручных повторов.
    """
    retry_of_id: Annotated[
        str | None,
        Field(
            pattern="^anl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Retry Of Id",
        ),
    ] = None
    """
    Исходный запуск при повторе.
    """
    retryable: Annotated[bool, Field(title="Retryable")]
    """
    Разрешён ручной повтор ошибки, включая provider_result_unknown.
    """


class AnalysisRunItemExecution(BaseModel):
    """
    Параметры выполнения для AnalysisRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cancelled_at: Timestamp | None = None
    """
    Дата отмены.
    """
    cancelled_by: Annotated[str | None, Field(title="Cancelled By")] = None
    """
    Идентификатор отменившего пользователя.
    """
    created_at: Timestamp
    """
    Дата создания.
    """
    failed_at: Timestamp | None = None
    """
    Дата ошибки обработки.
    """
    finished_at: Timestamp | None = None
    """
    Дата окончания выполнения.
    """
    is_test: Annotated[bool | None, Field(title="Is Test")] = False
    """
    Платная проверка сценария.
    """
    started_at: Timestamp | None = None
    """
    Начало выполнения.
    """
    status: Annotated[
        Literal["queued", "processing", "completed", "failed", "cancelled"],
        Field(title="Status"),
    ]
    """
    Состояние ресурса.
    """
    worker: Annotated[str | None, Field(title="Worker")] = None
    """
    Безопасный технический идентификатор обработчика.
    """


class AnalysisRunItemRetry(BaseModel):
    """
    Повторы обработки для AnalysisRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    attempt_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Attempt Count")]
    """
    Число выполненных попыток.
    """
    max_attempts: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Max Attempts")]
    """
    Предельное число попыток.
    """
    next_attempt_at: Timestamp | None = None
    """
    Следующая попытка.
    """
    retry_count: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Retry Count")]
    """
    Количество ручных повторов.
    """
    retry_of_id: Annotated[
        str | None,
        Field(
            pattern="^anl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Retry Of Id",
        ),
    ] = None
    """
    Исходный запуск при повторе.
    """


class AnalysisRunItemSource(BaseModel):
    """
    Источник данных для AnalysisRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    recorded_at: Timestamp | None = None
    """
    Фактическая дата и время исходной записи; поле отсутствует, если дата не задана.
    """
    recording_id: Annotated[
        str,
        Field(
            pattern="^fl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Recording Id",
        ),
    ]
    """
    Идентификатор аудиозаписи.
    """
    transcript_id: Annotated[str, Field(title="Transcript Id")]
    """
    Идентификатор текста расшифровки.
    """


class AnalysisScenarioExecutionItemExecution(BaseModel):
    """
    Параметры выполнения для app__analysis__schemas__ScenarioExecutionItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    created_at: Timestamp
    """
    Дата создания.
    """
    finished_at: Timestamp | None = None
    """
    Дата окончания выполнения.
    """
    preparation_error_code: Annotated[str | None, Field(title="Preparation Error Code")] = None
    """
    Безопасный код ошибки подготовки пакета.
    """
    preparation_status: Annotated[
        Literal["pending", "preparing", "completed", "failed"] | None,
        Field(title="Preparation Status"),
    ] = "completed"
    """
    Этап подготовки пакета: ожидание, отбор и создание задач, завершение либо ошибка.
    """
    started_at: Timestamp | None = None
    """
    Начало выполнения.
    """
    status: Annotated[str, Field(title="Status")]
    """
    Состояние ресурса.
    """


class AnalysisScenarioItemAudit(BaseModel):
    """
    Сведения о создании и изменении для AnalysisScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cloned_from_id: Annotated[
        str | None,
        Field(
            pattern="^sca-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Cloned From Id",
        ),
    ] = None
    """
    Исходный сценарий клонирования.
    """
    created_at: Timestamp
    """
    Дата создания.
    """
    created_by: Annotated[str | None, Field(title="Created By")] = None
    """
    Автор создания.
    """
    updated_at: Timestamp
    """
    Дата последнего изменения.
    """


class AnalysisScenarioItemStatistics(BaseModel):
    """
    Сводные показатели для AnalysisScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    failed_runs: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Failed Runs")]
    """
    Число неуспешных запусков.
    """
    last_run_at: Timestamp | None = None
    """
    Последний запуск.
    """
    runs: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Runs")]
    """
    Число запусков.
    """
    success_runs: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Success Runs")]
    """
    Успешные запуски.
    """


class AnalysisScenarioItemSummaryGeneration(BaseModel):
    """
    Настройки формирования резюме для AnalysisScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    enabled: Annotated[bool, Field(title="Enabled")]
    """
    Генерация резюме включена.
    """
    model_settings: AnalysisSummaryModelSettings | None = None
    """
    Независимые параметры сэмплирования сводки; отсутствие в старом сценарии сохраняет наследование анализа. Таймаут не является настройкой сценария: STT всегда 600 секунд, LLM всегда 120 секунд; timeout_seconds и прежние алиасы запрещены.
    """
    prompt: Annotated[str | None, Field(title="Prompt")] = None
    """
    Инструкция резюме.
    """


class AnalysisSourceFilter(BaseModel):
    """
    Описывает фильтры источника анализа в именах параметров списка транскрибаций.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    created_from: Annotated[str | None, Field(title="Created From")] = None
    """
    Нижняя граница даты создания.
    """
    created_to: Annotated[str | None, Field(title="Created To")] = None
    """
    Верхняя граница даты создания.
    """
    file_id: Annotated[str | None, Field(title="File Id")] = None
    """
    Идентификатор исходной записи; прежний поисковый фильтр сохраняется.
    """
    has_diarization: Annotated[bool | None, Field(title="Has Diarization")] = None
    """
    Фактическое наличие непустых меток дикторов в результате транскрибации.
    """
    has_summary: Annotated[bool | None, Field(title="Has Summary")] = None
    """
    Резюме уже сформировано.
    """
    job_id: Annotated[str | None, Field(title="Job Id")] = None
    """
    Идентификатор пакетного выполнения.
    """
    metadata_filters: Annotated[list[MetadataFilter] | None, Field(title="Metadata Filters")] = None
    """
    Условия сравнения метаданных.
    """
    metadata_group: MetadataGroup | None = None
    """
    Дерево условий И/ИЛИ; не совмещается с непустым metadata_filters.
    """
    metadata_logic: Annotated[Literal["and", "or"] | None, Field(title="Metadata Logic")] = None
    """
    Связь плоских условий метаданных; по умолчанию И.
    """
    model: Annotated[list[str] | None, Field(title="Model")] = None
    """
    Модель либо фильтр моделей согласно типу поля.
    """
    only_without_analysis: Annotated[bool | None, Field(title="Only Without Analysis")] = False
    """
    Только транскрибации без успешного неаннулированного анализа по любому сценарию.
    """
    scenario: Annotated[list[str] | None, Field(title="Scenario")] = None
    """
    Отбор по сценариям.
    """
    search: Annotated[str | None, Field(title="Search")] = None
    """
    Поисковая строка.
    """
    source_scenario_id: Annotated[
        str | None,
        Field(
            pattern="^sct-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Source Scenario Id",
        ),
    ] = None
    """
    Прежний alias сценария источника. Используйте transcription_scenario_id; одновременно задавать разные значения нельзя.
    """
    status: Annotated[list[str] | None, Field(title="Status")] = None
    """
    Состояние ресурса.
    """
    transcription_id: Annotated[str | None, Field(title="Transcription Id")] = None
    """
    Прежний фильтр текста расшифровки.
    """
    transcription_scenario_id: Annotated[
        str | None,
        Field(
            pattern="^sct-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Transcription Scenario Id",
        ),
    ] = None
    """
    Идентификатор сценария распознавания.
    """
    type: Annotated[str | None, Field(title="Type")] = "all"
    """
    Тип ресурса или настройки.
    """
    words_from: Annotated[int | None, Field(ge=0, le=2147483647, title="Words From")] = None
    """
    Минимум слов.
    """
    words_to: Annotated[int | None, Field(ge=0, le=2147483647, title="Words To")] = None
    """
    Максимум слов.
    """


class AnalysisTemplateItem(BaseModel):
    """
    Локализованная неизменяемая редакция универсального критерия.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    category: Annotated[str, Field(title="Category")]
    """
    Категория услуги или шаблона.
    """
    category_label: Annotated[str, Field(title="Category Label")]
    """
    Название категории.
    """
    description: Annotated[str, Field(title="Description")]
    """
    Описание.
    """
    id: Annotated[str, Field(title="Id")]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    locale: Annotated[str, Field(title="Locale")]
    """
    Язык шаблона.
    """
    name: Annotated[str, Field(title="Name")]
    """
    Название.
    """
    question: AnalysisQuestionInput
    """
    Критерий или его подпись.
    """
    version: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Version")]
    """
    Версия ресурса или схемы.
    """


class AnalysisTemplateItemResponse(BaseModel):
    """
    Типизированное сообщение AnalysisTemplateItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    template: AnalysisTemplateItem
    """
    Типизированное представление ресурса.
    """


class AnalysisTemplateList(BaseModel):
    """
    Актуальные редакции каталога с учётом выбранной категории.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    pagination: Pagination
    """
    Метаданные страницы.
    """
    templates: Annotated[list[AnalysisTemplateItem], Field(title="Templates")]
    """
    Типизированная коллекция результатов соответствующего домена.
    """


class AnswerCriterion(BaseModel):
    """
    Неизменный снимок критерия для отображения ответа и отклонения.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    additional_prompt: Annotated[str | None, Field(title="Additional Prompt")] = None
    """
    Необязательный промпт этого определения критерия; пустое значение эквивалентно отсутствию.
    """
    criterion_code: Annotated[
        str,
        Field(max_length=64, pattern="^[a-z][a-z0-9_]{0,63}$", title="Criterion Code"),
    ]
    """
    Код критерия на момент сохранения конфигурации.
    """
    criterion_id: Annotated[
        str,
        Field(
            pattern="^crit-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Criterion Id",
        ),
    ]
    """
    Постоянный идентификатор критерия Workspace в формате crit-UUID.
    """
    criterion_version: Annotated[int, Field(ge=1, title="Criterion Version")]
    """
    Неизменяемая версия определения критерия.
    """
    flag_when: Annotated[bool | None, Field(title="Flag When")] = None
    """
    Булево значение, означающее отклонение.
    """
    group_id: Annotated[str | None, Field(title="Group Id")] = None
    """
    ID группы в этом сценарии; null для критерия без группы.
    """
    options: Annotated[list[QuestionOption] | None, Field(title="Options")] = None
    """
    Варианты ответа из сохранённой версии сценария запуска.
    """
    severity: Annotated[Literal["none", "low", "medium", "high"], Field(title="Severity")]
    """
    Важность отклонения.
    """
    title: Annotated[str, Field(title="Title")]
    """
    Название критерия.
    """
    type: Annotated[Literal["boolean", "text", "list"], Field(title="Type")]
    """
    Тип ответа.
    """
    weight: Annotated[int | None, Field(ge=1, title="Weight")] = None
    """
    Сквозной порядковый номер 1..N, не коэффициент оценки.
    """


class AnswerValue1(BaseModel):
    """
    Ровно один вид ответа; protobuf oneof value. Список обёрнут в message, так как repeated нельзя поместить в oneof.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    boolean_value: Annotated[bool, Field(title="Boolean Value")]
    """
    Булев ответ, включая false.
    """
    selected_options: SelectedOptions | None = None
    """
    Выбранные варианты с кодами и историческими названиями; options=[] означает отсутствие выбора.
    """
    text_value: Annotated[str | None, Field(title="Text Value")] = None
    """
    Текстовый ответ, включая пустую строку.
    """


class AnswerValue2(BaseModel):
    """
    Ровно один вид ответа; protobuf oneof value. Список обёрнут в message, так как repeated нельзя поместить в oneof.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    boolean_value: Annotated[bool | None, Field(title="Boolean Value")] = None
    """
    Булев ответ, включая false.
    """
    selected_options: SelectedOptions | None = None
    """
    Выбранные варианты с кодами и историческими названиями; options=[] означает отсутствие выбора.
    """
    text_value: Annotated[str, Field(title="Text Value")]
    """
    Текстовый ответ, включая пустую строку.
    """


class AnswerValue3(BaseModel):
    """
    Ровно один вид ответа; protobuf oneof value. Список обёрнут в message, так как repeated нельзя поместить в oneof.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    boolean_value: Annotated[bool | None, Field(title="Boolean Value")] = None
    """
    Булев ответ, включая false.
    """
    selected_options: SelectedOptions
    """
    Выбранные варианты с кодами и историческими названиями; options=[] означает отсутствие выбора.
    """
    text_value: Annotated[str | None, Field(title="Text Value")] = None
    """
    Текстовый ответ, включая пустую строку.
    """


AnswerValue = TypeAliasType(
    "AnswerValue",
    Annotated[
        AnswerValue1 | AnswerValue2 | AnswerValue3,
        Field(
            examples=[{"selected_options": {"options": [{"key": "follow_up", "label": "Перезвонить"}]}}],
            title="AnswerValue",
        ),
    ],
)
"""
Ровно один вид ответа; protobuf oneof value. Список обёрнут в message, так как repeated нельзя поместить в oneof.
"""


class AudioInfo(BaseModel):
    """
    Типизированное сообщение AudioInfo.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    bit_depth: Annotated[int | None, Field(ge=0, le=2147483647, title="Bit Depth")] = None
    """
    Битовая глубина.
    """
    bitrate_kbps: Annotated[int | None, Field(ge=0, le=2147483647, title="Bitrate Kbps")] = None
    """
    Битрейт, килобиты в секунду.
    """
    bitrate_mode: Annotated[str | None, Field(title="Bitrate Mode")] = None
    """
    Режим битрейта.
    """
    channel_layout: Annotated[str | None, Field(title="Channel Layout")] = None
    """
    Расположение каналов.
    """
    channels: Annotated[int | None, Field(ge=0, le=2147483647, title="Channels")] = None
    """
    Количество каналов.
    """
    codec: Annotated[str | None, Field(title="Codec")] = None
    """
    Кодек.
    """
    container_format: Annotated[str | None, Field(title="Container Format")] = None
    """
    Контейнер, например MP3.
    """
    duration_seconds: Annotated[float | None, Field(ge=0.0, title="Duration Seconds")] = None
    """
    Точная длительность из аудиодиагностики, секунды.
    """
    encoder: Annotated[str | None, Field(title="Encoder")] = None
    """
    Имя кодировщика.
    """
    original_created_at: Annotated[str | None, Field(title="Original Created At")] = None
    """
    Исходный текст даты из тегов; может не быть RFC 3339.
    """
    quality: AudioQuality | None = None
    """
    Диагностика качества аудио.
    """
    sample_format: Annotated[Literal["integer", "float"] | None, Field(title="Sample Format")] = None
    """
    Формат отсчётов: целочисленный или с плавающей точкой.
    """
    sample_rate_hz: Annotated[int | None, Field(ge=0, le=2147483647, title="Sample Rate Hz")] = None
    """
    Частота дискретизации, Гц.
    """
    tags: StringMap | None = None
    """
    Произвольные строковые теги аудиофайла.
    """


class Evidence(BaseModel):
    """
    Типизированное сообщение Evidence.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    absolute_time_range: TimeRange | None = None
    """
    Абсолютное положение цитаты в исходном аудио.
    """
    speaker_id: Annotated[str | None, Field(title="Speaker Id")] = None
    """
    Идентификатор говорящего.
    """
    text: Annotated[str, Field(title="Text")]
    """
    Подтверждающий фрагмент текста расшифровки.
    """
    time_range: TimeRange
    """
    Смещения в исходном аудио, секунды.
    """


JsonObject = TypeAliasType("JsonObject", dict[str, JsonValue])
"""
Произвольный JSON-объект, protobuf Struct. Ключи определяет интеграция, а не API.
"""


JsonObjectInput = TypeAliasType("JsonObjectInput", dict[str, JsonValue])
"""
Произвольный JSON-объект, protobuf Struct. Ключи определяет интеграция, а не API.
"""


JsonObjectOutput = TypeAliasType("JsonObjectOutput", dict[str, JsonValue])
"""
Произвольный JSON-объект, protobuf Struct. Ключи определяет интеграция, а не API.
"""


class ModelSettings(BaseModel):
    """
    Типизированное сообщение ModelSettings.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    provider_options: JsonObjectOutput | None = None
    """
    Остальные разрешённые параметры выбранной модели, проверяемые её каталогом.
    """
    temperature: Annotated[float | None, Field(title="Temperature")] = None
    """
    Температура генерации; допустимый диапазон определяется моделью.
    """
    top_p: Annotated[float | None, Field(ge=0.0, le=1.0, title="Top P")] = None
    """
    Параметр top-p.
    """


class ProviderOptions(BaseModel):
    """
    Типизированное сообщение ProviderOptions.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    values: JsonObjectOutput
    """
    Параметры конкретного провайдера; схема проверяется по каталогу выбранной модели.
    """


class RecognitionSettings(BaseModel):
    """
    Типизированное сообщение RecognitionSettings.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    diarization: Annotated[bool | None, Field(title="Diarization")] = None
    """
    Разделение по говорящим.
    """
    language: Annotated[str | None, Field(title="Language")] = None
    """
    Код языка распознавания.
    """
    provider_options: JsonObjectOutput | None = None
    """
    Разрешённые параметры STT, не вошедшие в общие поля. Существующие ключи сохраняются.
    """
    punctuation: Annotated[bool | None, Field(title="Punctuation")] = None
    """
    Автоматическая пунктуация.
    """


class RecordingImportAudio(BaseModel):
    """
    Фактическое начало импортируемой записи.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    recorded_at: Timestamp | None = None
    """
    Фактическое начало записи, ISO 8601 с часовым поясом.
    """


class RecordingItemAudio(BaseModel):
    """
    Параметры аудиозаписи для RecordingItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    duration_seconds: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Duration Seconds")] = None
    """
    Длительность, секунды.
    """
    recorded_at: Timestamp | None = None
    """
    Время записи разговора.
    """
    technical: AudioInfo | None = None
    """
    Результат технического анализа аудио; отсутствует до готовности.
    """


class RecordingItemFile(BaseModel):
    """
    Свойства файла для RecordingItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    checksum: Annotated[str | None, Field(title="Checksum")] = None
    """
    Контрольная сумма файла.
    """
    checksum_algorithm: Annotated[str, Field(title="Checksum Algorithm")]
    """
    Алгоритм контрольной суммы.
    """
    download_url: Annotated[str | None, Field(title="Download Url")] = None
    """
    Авторизованный HTTP-путь скачивания; внутренний storage URL не раскрывается.
    """
    filename: Annotated[str, Field(title="Filename")]
    """
    Имя файла.
    """
    mime_type: Annotated[str | None, Field(title="Mime Type")] = None
    """
    MIME-тип аудиофайла.
    """
    size_bytes: UInt64Value | None = None
    """
    Размер файла в байтах.
    """


class RecordingItemImportState(BaseModel):
    """
    Состояние импорта для RecordingItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    attempt_count: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Attempt Count")] = 0
    """
    Число попыток импорта.
    """
    downloaded_at: Timestamp | None = None
    """
    Дата успешного скачивания.
    """
    error_code: Annotated[str | None, Field(title="Error Code")] = None
    """
    Безопасный машинный код ошибки импорта.
    """
    error_message: Annotated[str | None, Field(title="Error Message")] = None
    """
    Безопасное пояснение ошибки импорта.
    """
    next_attempt_at: Timestamp | None = None
    """
    Дата следующей попытки импорта.
    """


class RecordingItemProcessing(BaseModel):
    """
    Состояние обработки для RecordingItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    finished_at: Timestamp | None = None
    """
    Завершение обработки файла.
    """
    started_at: Timestamp | None = None
    """
    Начало обработки файла.
    """
    status: Annotated[
        Literal[
            "download_pending",
            "downloading",
            "download_retry_wait",
            "download_failed",
            "duplicate",
            "queued",
            "processing",
            "completed",
            "failed",
            "deleted",
        ],
        Field(title="Status"),
    ]
    """
    Статус записи; duplicate означает отклонённый по checksum импорт без сохранённого исходника.
    """


class RecordingItemStorage(BaseModel):
    """
    Хранение и срок удаления для RecordingItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    annulled_at: Timestamp | None = None
    """
    Дата аннулирования записи.
    """
    annulled_by_user_id: Annotated[str | None, Field(title="Annulled By User Id")] = None
    """
    Идентификатор пользователя, аннулировавшего запись.
    """
    deleted_at: Timestamp | None = None
    """
    Дата удаления.
    """
    deleted_by: Annotated[str | None, Field(title="Deleted By")] = None
    """
    Идентификатор удалившего пользователя.
    """
    is_annulled: Annotated[bool | None, Field(title="Is Annulled")] = False
    """
    Запись исключена из дальнейшей работы; удаление аудио само по себе её не аннулирует.
    """
    retention_expires_at: Timestamp | None = None
    """
    Дата планового удаления исходника.
    """
    retention_hours: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Retention Hours")] = None
    """
    Зафиксированный срок хранения, часы.
    """
    uploaded_at: Timestamp
    """
    Время загрузки в хранилище.
    """


class RecordingStatistics(BaseModel):
    """
    Типизированное сообщение RecordingStatistics.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    status_counts: IntegerMap
    """
    Количество записей по состояниям, включая deleted.
    """
    total_count: UInt64Value
    """
    Количество записей во всей отфильтрованной выборке.
    """
    total_duration_seconds: Annotated[float, Field(ge=0.0, title="Total Duration Seconds")]
    """
    Суммарная длительность отфильтрованных записей, секунды.
    """
    total_size_bytes: UInt64Value
    """
    Байты живых исходников, исключая удалённые файлы.
    """


class RecordingUpdateAudio(BaseModel):
    """
    Параметры аудиозаписи для RecordingUpdate.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    recorded_at: Timestamp | None = None
    """
    Время записи разговора.
    """


class TokenUsage(BaseModel):
    """
    Типизированное сообщение TokenUsage.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cached_input_tokens: UInt64Value | None = None
    """
    Закэшированные входные токены, если доступны.
    """
    input_tokens: UInt64Value
    """
    Входные токены.
    """
    output_tokens: UInt64Value
    """
    Выходные токены.
    """
    reasoning_tokens: UInt64Value | None = None
    """
    Токены рассуждения, если доступны.
    """
    total_tokens: UInt64Value
    """
    Всего токенов.
    """


class TranscriptContent(BaseModel):
    """
    Типизированное сообщение TranscriptContent.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    has_diarization: Annotated[bool | None, Field(title="Has Diarization")] = False
    """
    В сегментах или словах результата есть непустые метки дикторов, включая ID 0.
    """
    language: Annotated[str, Field(title="Language")]
    """
    Код языка, возвращённый распознаванием.
    """
    search_results: Annotated[list[TranscriptSearchResult], Field(title="Search Results")]
    """
    Результаты настроенного поиска фраз.
    """
    segments: Annotated[list[TranscriptSegment], Field(title="Segments")]
    """
    Сегменты в порядке аудиозаписи.
    """
    words: Annotated[list[TranscriptWord], Field(title="Words")]
    """
    Слова; пустой список, если провайдер не выдаёт пословные таймкоды.
    """


class TranscriptItem(BaseModel):
    """
    Текст расшифровки с типизированным содержимым, резюме и статистикой.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    content: TranscriptContent
    """
    Содержимое ресурса.
    """
    id: Annotated[str, Field(title="Id")]
    """
    Идентификатор текста расшифровки.
    """
    is_annulled: Annotated[bool | None, Field(title="Is Annulled")] = False
    """
    Текст расшифровки необратимо аннулирован.
    """
    recording_id: Annotated[
        str,
        Field(
            pattern="^fl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Recording Id",
        ),
    ]
    """
    Идентификатор аудиозаписи.
    """
    statistics: TextStatistics
    """
    Сводные показатели.
    """
    summary: TranscriptSummary
    """
    Резюме, тип определяется схемой.
    """
    transcription_run_id: Annotated[
        str,
        Field(
            pattern="^trn-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Transcription Run Id",
        ),
    ]
    """
    Идентификатор запуска транскрибации.
    """


class TranscriptItemResponse(BaseModel):
    """
    Типизированное сообщение TranscriptItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    transcript: TranscriptItem
    """
    Типизированное представление ресурса.
    """


class TranscriptionRunItemSource(BaseModel):
    """
    Источник данных для TranscriptionRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    download_url: Annotated[str | None, Field(title="Download Url")] = None
    """
    Защищённая ссылка на исходное аудио; отсутствует для удалённого или недоступного файла.
    """
    duration_seconds: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Duration Seconds")] = None
    """
    Длительность, секунды.
    """
    filename: Annotated[str | None, Field(title="Filename")] = None
    """
    Имя файла.
    """
    metadata: JsonObjectOutput | None = None
    """
    Пользовательские либо доменные метаданные; известный системный контракт не скрывается здесь.
    """
    origin: Annotated[str | None, Field(title="Origin")] = None
    """
    Источник записи.
    """
    recorded_at: Timestamp | None = None
    """
    Фактическая дата и время исходной записи; поле отсутствует, если дата не задана.
    """
    recording_id: Annotated[
        str,
        Field(
            pattern="^fl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Recording Id",
        ),
    ]
    """
    Идентификатор аудиозаписи.
    """
    recording_status: Annotated[str | None, Field(title="Recording Status")] = None
    """
    Состояние исходного файла, включая deleted.
    """


class TranscriptionScenarioExecutionItem(BaseModel):
    """
    Агрегированный результат пакетного запуска сценария.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    execution: TranscriptionScenarioExecutionItemExecution
    """
    Параметры выполнения
    """
    id: Annotated[str, Field(title="Id")]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    scenario_id: Annotated[
        str,
        Field(
            pattern="^sct-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Scenario Id",
        ),
    ]
    """
    Идентификатор сценария.
    """
    scenario_type: Annotated[str, Field(title="Scenario Type")]
    """
    Домен сценария.
    """
    statistics: TranscriptionScenarioExecutionItemStatistics
    """
    Сводные показатели
    """
    trigger_type: Annotated[Literal["manual", "auto", "scheduled"], Field(title="Trigger Type")]
    """
    Способ запуска сценария.
    """


class TranscriptionScenarioExecutionItemResponse(BaseModel):
    """
    Типизированное сообщение app__transcription__schemas__ScenarioExecutionItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    execution: TranscriptionScenarioExecutionItem
    """
    Состояние выполнения.
    """


class TranscriptionScenarioExecutionList(BaseModel):
    """
    Возвращает страницу истории пакетных запусков.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    executions: Annotated[list[TranscriptionScenarioExecutionItem], Field(title="Executions")]
    """
    Типизированная коллекция результатов соответствующего домена.
    """
    pagination: Pagination
    """
    Метаданные страницы.
    """


class TranscriptionScenarioItemRecognition(BaseModel):
    """
    Настройки распознавания для TranscriptionScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    advanced_settings: ProviderOptions
    """
    Дополнительные настройки выбранного провайдера. Таймаут не является настройкой сценария: STT всегда 600 секунд, LLM всегда 120 секунд; timeout_seconds и прежние алиасы запрещены.
    """
    model_id: Annotated[str, Field(title="Model Id")]
    """
    Идентификатор модели.
    """
    provider: Annotated[str, Field(title="Provider")]
    """
    Код провайдера.
    """
    settings: RecognitionSettings
    """
    Настройки модели. Таймаут не является настройкой сценария: STT всегда 600 секунд, LLM всегда 120 секунд; timeout_seconds и прежние алиасы запрещены.
    """
    stt_model_id: Annotated[str, Field(title="Stt Model Id")]
    """
    Идентификатор STT-модели.
    """


class TranscriptionScenarioItemSummaryGeneration(BaseModel):
    """
    Настройки формирования резюме для TranscriptionScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    advanced_settings: ProviderOptions | None = None
    """
    Дополнительные настройки LLM резюме. Таймаут не является настройкой сценария: STT всегда 600 секунд, LLM всегда 120 секунд; timeout_seconds и прежние алиасы запрещены.
    """
    enabled: Annotated[bool, Field(title="Enabled")]
    """
    Генерация резюме включена.
    """
    llm_model_id: Annotated[str | None, Field(title="Llm Model Id")] = None
    """
    LLM-модель резюме.
    """
    model_settings: ModelSettings | None = None
    """
    Настройки LLM резюме. Таймаут не является настройкой сценария: STT всегда 600 секунд, LLM всегда 120 секунд; timeout_seconds и прежние алиасы запрещены.
    """


class UploadRecordingForm(BaseModel):
    """
    Типизированное сообщение UploadRecordingForm.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    check_duplicates: bool | None = True
    """
    Проверять SHA-256 среди неудалённых исходников текущего Workspace. false разрешает повторную загрузку.
    """
    file: bytes
    """
    Аудиофайл; бинарная часть multipart, для gRPC — bytes или поток.
    """
    metadata: JsonObject | None = None
    """
    Ключи верхнего уровня metadata: от 1 до 64 символов, только строчные a-z, цифры 0-9 и _. Проверяется полная исходная строка без нормализации; цифра и _ допустимы в начале. Значения и ключи вложенных объектов этим правилом не ограничены. Неподходящий ключ возвращает 422 до сохранения и постановки задачи.
    """
    recorded_at: Timestamp | None = None
    """
    Фактическое начало записи, ISO 8601 с часовым поясом.
    """
    retention_days: Annotated[int | None, Field(ge=1, le=2147483647)] = None
    """
    Срок хранения, дни; минимум 1.
    """


class WorkspaceItem(BaseModel):
    """
    DTO workspace в списке доступных контуров.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    access: WorkspaceItemAccess
    """
    Права и доступность
    """
    audit: WorkspaceItemAudit
    """
    Сведения о создании и изменении
    """
    description: Annotated[str | None, Field(title="Description")] = None
    """
    Описание.
    """
    id: Annotated[
        str,
        Field(
            pattern="^ws-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Id",
        ),
    ]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    name: Annotated[str, Field(title="Name")]
    """
    Название.
    """
    subscriber_id: Annotated[str | None, Field(title="Subscriber Id")] = None
    """
    Идентификатор финансовой организации (абонента).
    """


class WorkspaceList(BaseModel):
    """
    Список workspace текущего пользователя.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    workspaces: Annotated[list[WorkspaceItem], Field(title="Workspaces")]
    """
    Типизированная коллекция результатов соответствующего домена.
    """


class WorkspaceOverviewBilling(BaseModel):
    """
    Финансовые сведения для WorkspaceOverview.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    balance: WorkspaceBalance
    """
    Точный баланс счёта.
    """
    current_period_cost: Annotated[
        str | None,
        Field(pattern="^-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?$", title="Current Period Cost"),
    ] = None
    """
    Точные расходы текущего периода.
    """
    plan: WorkspaceOverviewPlan


class AnalysisAnswer(BaseModel):
    """
    Типизированное сообщение AnalysisAnswer.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    confidence: Annotated[float | None, Field(ge=0.0, le=1.0, title="Confidence")] = None
    """
    Уверенность модели.
    """
    criterion: AnswerCriterion
    """
    Снимок критерия из запуска.
    """
    evidence: Annotated[list[Evidence], Field(title="Evidence")]
    """
    Подтверждающие цитаты.
    """
    explanation: Annotated[str | None, Field(title="Explanation")] = None
    """
    Объяснение ответа.
    """
    is_critical: Annotated[bool | None, Field(title="Is Critical")] = False
    """
    Отклонение по правилу исторического критерия; вычисляется сервером.
    """
    value: AnswerValue
    """
    Типизированное значение.
    """


class AnalysisCriterionSearchResponse(BaseModel):
    """
    До пяти актуальных критериев текущего Workspace для повторного использования.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    criteria: Annotated[list[AnalysisQuestion], Field(title="Criteria")]
    """
    Найденные вопросы с постоянной идентичностью и актуальным определением.
    """


class AnalysisResultItemResult(BaseModel):
    """
    Результат выполнения для AnalysisResultItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    answers: Annotated[list[AnalysisAnswer], Field(title="Answers")]
    """
    Типизированные ответы на критерии.
    """
    criterion_groups: Annotated[
        list[AnalysisCriterionGroup] | None,
        Field(title="Criterion Groups", validate_default=True),
    ] = []
    """
    Группы в сохранённом порядке; для результата из исторического снимка.
    """
    is_annulled: Annotated[bool, Field(title="Is Annulled")]
    """
    Необратимый признак аннулирования результата; ответы и резюме сохраняются.
    """
    summary: Annotated[str | None, Field(title="Summary")] = None
    """
    Резюме, тип определяется схемой.
    """


class AnalysisResultItemUsage(BaseModel):
    """
    Объём использования для AnalysisResultItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    token_usage: TokenUsage
    """
    Количество использованных токенов.
    """


class AnalysisRunDetailBilling(BaseModel):
    """
    Финансовые сведения для AnalysisRunDetail.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cost: Annotated[str, Field(pattern="^-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?$", title="Cost")]
    """
    Полная сохранённая стоимость анализа в рублях до скидок и грантов.
    """
    estimated_cost: Annotated[
        str | None,
        Field(pattern="^-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?$", title="Estimated Cost"),
    ] = None
    """
    Предварительная точная оценка стоимости.
    """
    token_cost: TokenCostBreakdown
    token_usage: TokenUsage
    """
    Количество использованных токенов.
    """


class AnalysisRunDetailResult(BaseModel):
    """
    Результат выполнения для AnalysisRunDetail.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    answers: Annotated[list[AnalysisAnswer], Field(title="Answers")]
    """
    Типизированные ответы на критерии.
    """
    criterion_groups: Annotated[
        list[AnalysisCriterionGroup] | None,
        Field(title="Criterion Groups", validate_default=True),
    ] = []
    """
    Группы в сохранённом порядке; для результата из исторического снимка.
    """
    is_annulled: Annotated[bool, Field(title="Is Annulled")]
    """
    Необратимый признак аннулирования результата; ответы и резюме сохраняются.
    """
    result_id: Annotated[str | None, Field(title="Result Id")] = None
    """
    Идентификатор результата, если он создан.
    """
    summary: Annotated[str | None, Field(title="Summary")] = None
    """
    Резюме, тип определяется схемой.
    """
    summary_status: Annotated[str, Field(title="Summary Status")]
    """
    Состояние генерации резюме.
    """


class AnalysisRunDetailSource(BaseModel):
    """
    Источник данных для AnalysisRunDetail.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    download_url: Annotated[str | None, Field(title="Download Url")] = None
    """
    Защищённая ссылка на исходное аудио; отсутствует для удалённого или недоступного файла.
    """
    duration_seconds: Annotated[int | None, Field(ge=-2147483648, le=2147483647, title="Duration Seconds")] = None
    """
    Длительность, секунды.
    """
    metadata: JsonObjectOutput
    """
    Пользовательские либо доменные метаданные; известный системный контракт не скрывается здесь.
    """
    recorded_at: Timestamp | None = None
    """
    Фактическая дата и время исходной записи; поле отсутствует, если дата не задана.
    """
    recording_id: Annotated[
        str,
        Field(
            pattern="^fl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Recording Id",
        ),
    ]
    """
    Идентификатор аудиозаписи.
    """
    recording_status: Annotated[str | None, Field(title="Recording Status")] = None
    """
    Состояние исходного файла, включая deleted.
    """
    transcript_id: Annotated[str, Field(title="Transcript Id")]
    """
    Идентификатор текста расшифровки.
    """
    transcription_run_id: Annotated[
        str,
        Field(
            pattern="^trn-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Transcription Run Id",
        ),
    ]
    """
    Идентификатор запуска транскрибации.
    """


class AnalysisRunItemBilling(BaseModel):
    """
    Финансовые сведения для AnalysisRunItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    cost: Annotated[str, Field(pattern="^-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?$", title="Cost")]
    """
    Полная сохранённая стоимость анализа в рублях до скидок и грантов.
    """
    estimated_cost: Annotated[
        str | None,
        Field(pattern="^-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?$", title="Estimated Cost"),
    ] = None
    """
    Предварительная точная оценка стоимости.
    """
    token_usage: TokenUsage
    """
    Количество использованных токенов.
    """


class AnalysisScenarioExecutionItem(BaseModel):
    """
    Агрегированный результат пакетного запуска сценария.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    execution: AnalysisScenarioExecutionItemExecution
    """
    Параметры выполнения
    """
    id: Annotated[str, Field(title="Id")]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    scenario_id: Annotated[
        str,
        Field(
            pattern="^sca-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Scenario Id",
        ),
    ]
    """
    Идентификатор сценария.
    """
    scenario_type: Annotated[str, Field(title="Scenario Type")]
    """
    Домен сценария.
    """
    statistics: AnalysisScenarioExecutionItemStatistics
    """
    Сводные показатели
    """
    trigger_type: Annotated[Literal["manual", "auto", "scheduled"], Field(title="Trigger Type")]
    """
    Способ запуска сценария.
    """


class AnalysisScenarioExecutionItemResponse(BaseModel):
    """
    Типизированное сообщение app__analysis__schemas__ScenarioExecutionItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    execution: AnalysisScenarioExecutionItem
    """
    Состояние выполнения.
    """


class AnalysisScenarioExecutionList(BaseModel):
    """
    Возвращает страницу пакетных исполнений сценария.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    executions: Annotated[list[AnalysisScenarioExecutionItem], Field(title="Executions")]
    """
    Типизированная коллекция результатов соответствующего домена.
    """
    pagination: Pagination
    """
    Метаданные страницы.
    """


class AnalysisScenarioItemAnalysis(BaseModel):
    """
    Настройки анализа для AnalysisScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    advanced_settings: ProviderOptions
    """
    Дополнительные настройки выбранного провайдера. Таймаут не является настройкой сценария: STT всегда 600 секунд, LLM всегда 120 секунд; timeout_seconds и прежние алиасы запрещены.
    """
    criterion_groups: Annotated[
        list[AnalysisCriterionGroup] | None,
        Field(title="Criterion Groups", validate_default=True),
    ] = []
    """
    Группы в сохранённом порядке; для результата из исторического снимка.
    """
    llm_model_id: Annotated[str, Field(title="Llm Model Id")]
    """
    Идентификатор LLM-модели.
    """
    model_settings: ModelSettings
    """
    Настройки выбранной LLM-модели. Таймаут не является настройкой сценария: STT всегда 600 секунд, LLM всегда 120 секунд; timeout_seconds и прежние алиасы запрещены.
    """
    pre_prompt: Annotated[str | None, Field(title="Pre Prompt")] = None
    """
    Инструкция перед критериями.
    """
    questions: Annotated[list[AnalysisQuestion], Field(title="Questions")]
    """
    Критерии с уникальными ключами.
    """


class AnalysisScenarioItemTrigger(BaseModel):
    """
    Условия запуска для AnalysisScenarioItem.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    schedule: ScenarioSchedule | None = None
    """
    Расписание, формат определяется схемой.
    """
    source_filter: AnalysisSourceFilter
    """
    Условия отбора текстов расшифровки.
    """
    trigger_type: Annotated[Literal["manual", "auto", "scheduled"], Field(title="Trigger Type")]
    """
    Способ запуска сценария.
    """


class ApiError(BaseModel):
    """
    Типизированное сообщение ApiError.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    code: Annotated[str, Field(title="Code")]
    """
    Стабильный доменный код; не HTTP-код и не имя исключения.
    """
    details: JsonObjectOutput | None = None
    """
    Безопасные дополнительные сведения, например поддерживаемые форматы.
    """
    message: Annotated[str, Field(title="Message")]
    """
    Безопасное сообщение на русском языке.
    """
    request_id: Annotated[str | None, Field(title="Request Id")] = None
    """
    Технический идентификатор обращения; без секретов и пользовательских данных.
    """
    violations: Annotated[list[FieldViolation], Field(title="Violations")]
    """
    Ошибки полей; пустой массив при отсутствии.
    """


class ErrorResponse(BaseModel):
    """
    Типизированное сообщение ErrorResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    error: ApiError
    """
    Безопасные сведения об ошибке.
    """


class RecordingImport(BaseModel):
    """
    Запрос асинхронного скачивания аудиофайла по прямой ссылке.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    audio: RecordingImportAudio | None = None
    """
    Фактическое время записи.
    """
    check_duplicates: Annotated[bool | None, Field(title="Check Duplicates")] = True
    """
    Проверять SHA-256 среди неудалённых исходников текущего Workspace. false разрешает повторную загрузку.
    """
    file: RecordingImportFile
    """
    Свойства файла
    """
    metadata: JsonObjectInput | None = None
    """
    Ключи верхнего уровня metadata: от 1 до 64 символов, только строчные a-z, цифры 0-9 и _. Проверяется полная исходная строка без нормализации; цифра и _ допустимы в начале. Значения и ключи вложенных объектов этим правилом не ограничены. Неподходящий ключ возвращает 422 до сохранения и постановки задачи.
    """
    storage: RecordingImportStorage | None = None
    """
    Хранение и срок удаления
    """


class RecordingItem(BaseModel):
    """
    Аудиозапись: файл, аудиодиагностика, хранение, обработка, импорт и статистика.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    audio: RecordingItemAudio | None = None
    """
    Параметры аудиозаписи
    """
    file: RecordingItemFile
    """
    Свойства файла
    """
    id: Annotated[
        str,
        Field(
            pattern="^fl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Id",
        ),
    ]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    import_state: RecordingItemImportState | None = None
    """
    Состояние импорта
    """
    metadata: JsonObjectOutput
    """
    Пользовательские либо доменные метаданные; известный системный контракт не скрывается здесь.
    """
    processing: RecordingItemProcessing
    """
    Состояние обработки
    """
    source: Annotated[str, Field(title="Source")]
    """
    Источник записи.
    """
    statistics: RecordingItemStatistics
    """
    Сводные показатели
    """
    storage: RecordingItemStorage
    """
    Хранение и срок удаления
    """


class RecordingItemResponse(BaseModel):
    """
    Типизированное сообщение RecordingItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    recording: RecordingItem
    """
    Типизированное представление ресурса.
    """


class RecordingList(BaseModel):
    """
    Cursor-страница списка аудиозаписей.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    pagination: Pagination
    """
    Метаданные страницы.
    """
    recordings: Annotated[list[RecordingItem], Field(title="Recordings")]
    """
    Типизированная коллекция результатов соответствующего домена.
    """
    statistics: RecordingStatistics
    """
    Сводные показатели.
    """


class RecordingUpdate(BaseModel):
    """
    Запрос изменения пользовательских полей аудиозаписи.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    audio: RecordingUpdateAudio | None = None
    """
    Параметры аудиозаписи
    """
    file: RecordingUpdateFile | None = None
    """
    Свойства файла
    """
    metadata: JsonObjectInput | None = None
    """
    Ключи верхнего уровня metadata: от 1 до 64 символов, только строчные a-z, цифры 0-9 и _. Проверяется полная исходная строка без нормализации; цифра и _ допустимы в начале. Значения и ключи вложенных объектов этим правилом не ограничены. Прежний неподходящий ключ можно удалить или передать с неизменным JSON-значением; изменение его значения и добавление новых неподходящих ключей возвращают 422. Чтение и фильтрация прежних ключей сохраняются.
    """
    update_mask: Annotated[str, Field(min_length=1, title="Update Mask")]
    """
    Обязательная маска изменяемых полей через запятую, пути в lowerCamelCase как в ProtoJSON FieldMask. В JSON payload имена snake_case. Поле в маске без значения сбрасывает optional-поле; для repeated/map в маске отсутствие значения означает []/{}. Обязательные поля сбрасывать нельзя.
    """


class TranscriptionRunItem(BaseModel):
    """
    Публичное представление запуска транскрибации.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    billing: TranscriptionRunItemBilling
    """
    Финансовые сведения
    """
    error: TranscriptionRunItemError | None = None
    """
    Сведения об ошибке
    """
    execution: TranscriptionRunItemExecution
    """
    Параметры выполнения
    """
    id: Annotated[
        str,
        Field(
            pattern="^trn-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Id",
        ),
    ]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    model: TranscriptionRunItemModel
    """
    Выбранная модель
    """
    result: TranscriptionRunItemResult | None = None
    """
    Результат выполнения
    """
    retry: TranscriptionRunItemRetry | None = None
    """
    Повторы обработки
    """
    source: TranscriptionRunItemSource
    """
    Источник данных
    """
    statistics: TranscriptionRunItemStatistics | None = None
    """
    Сводные показатели
    """


class TranscriptionRunItemResponse(BaseModel):
    """
    Типизированное сообщение TranscriptionRunItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    run: TranscriptionRunItem
    """
    Типизированное представление ресурса.
    """


class TranscriptionRunList(BaseModel):
    """
    Страница запусков с общим количеством и распределением статусов.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    pagination: Pagination
    """
    Метаданные страницы.
    """
    runs: Annotated[list[TranscriptionRunItem], Field(title="Runs")]
    """
    Число запусков.
    """
    statistics: RunStatistics
    """
    Сводные показатели.
    """


class TranscriptionScenarioItem(BaseModel):
    """
    Публичное представление сценария транскрибации.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    active: Annotated[bool, Field(title="Active")]
    """
    Активность.
    """
    audit: TranscriptionScenarioItemAudit
    """
    Сведения о создании и изменении
    """
    description: Annotated[str | None, Field(title="Description")] = None
    """
    Описание.
    """
    id: Annotated[
        str,
        Field(
            pattern="^sct-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Id",
        ),
    ]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    name: Annotated[str, Field(title="Name")]
    """
    Название.
    """
    recognition: TranscriptionScenarioItemRecognition
    """
    Настройки распознавания
    """
    statistics: TranscriptionScenarioItemStatistics
    """
    Сводные показатели
    """
    status: Annotated[str, Field(title="Status")]
    """
    Состояние ресурса.
    """
    summary_generation: TranscriptionScenarioItemSummaryGeneration
    """
    Настройки формирования резюме
    """
    trigger: TranscriptionScenarioItemTrigger
    """
    Условия запуска
    """


class TranscriptionScenarioItemResponse(BaseModel):
    """
    Типизированное сообщение TranscriptionScenarioItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    scenario: TranscriptionScenarioItem
    """
    Отбор по сценариям.
    """


class TranscriptionScenarioList(BaseModel):
    """
    Возвращает страницу сценариев транскрибации с общим количеством.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    pagination: Pagination
    """
    Метаданные страницы.
    """
    scenarios: Annotated[list[TranscriptionScenarioItem], Field(title="Scenarios")]
    """
    Типизированная коллекция результатов соответствующего домена.
    """


class WorkspaceOverview(BaseModel):
    """
    Агрегированный обзор workspace.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    billing: WorkspaceOverviewBilling
    """
    Финансовые сведения
    """
    statistics: WorkspaceOverviewStatistics
    """
    Сводные показатели
    """
    status: Annotated[str, Field(title="Status")]
    """
    Состояние ресурса.
    """
    workspace_id: Annotated[
        str,
        Field(
            pattern="^ws-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Workspace Id",
        ),
    ]
    """
    Идентификатор Workspace; обязательна проверка доступа.
    """


class AnalysisResultItem(BaseModel):
    """
    Публичное представление результата анализа.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    created_at: Timestamp
    """
    Дата создания.
    """
    id: Annotated[str, Field(title="Id")]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    recording: RecordingItem | None = None
    """
    Полная карточка аудиофайла с метаданными; возвращается только при include_recording=true.
    """
    result: AnalysisResultItemResult
    """
    Результат выполнения
    """
    source: AnalysisResultItemSource
    """
    Источник данных
    """
    statistics: AnalysisResultItemStatistics
    """
    Счётчики результата анализа.
    """
    usage: AnalysisResultItemUsage
    """
    Объём использования
    """


class AnalysisResultItemResponse(BaseModel):
    """
    Типизированное сообщение AnalysisResultItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    result: AnalysisResultItem
    """
    Типизированное представление ресурса.
    """


class AnalysisResultList(BaseModel):
    """
    Типизированное сообщение AnalysisResultList.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    pagination: Pagination
    """
    Метаданные страницы.
    """
    results: Annotated[list[AnalysisResultItem], Field(title="Results")]
    """
    Результаты анализа.
    """


class AnalysisRunDetail(BaseModel):
    """
    Полная карточка анализа с неизменным ID запуска и необязательным результатом.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    billing: AnalysisRunDetailBilling
    """
    Финансовые сведения
    """
    error: AnalysisRunDetailError | None = None
    """
    Сведения об ошибке
    """
    execution: AnalysisRunDetailExecution
    """
    Параметры выполнения
    """
    id: Annotated[
        str,
        Field(
            pattern="^anl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Id",
        ),
    ]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    model: AnalysisRunDetailModel
    """
    Выбранная модель
    """
    result: AnalysisRunDetailResult
    """
    Результат выполнения
    """
    retry: AnalysisRunDetailRetry
    """
    Повторы обработки
    """
    source: AnalysisRunDetailSource
    """
    Источник данных
    """
    statistics: AnalysisRunDetailStatistics
    """
    Сводные показатели
    """


class AnalysisRunDetailResponse(BaseModel):
    """
    Типизированное сообщение AnalysisRunDetailResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    run: AnalysisRunDetail
    """
    Типизированное представление ресурса.
    """


class AnalysisRunItem(BaseModel):
    """
    Публичное представление запуска анализа.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    billing: AnalysisRunItemBilling
    """
    Финансовые сведения
    """
    error: AnalysisRunItemError | None = None
    """
    Сведения об ошибке
    """
    execution: AnalysisRunItemExecution
    """
    Параметры выполнения
    """
    id: Annotated[
        str,
        Field(
            pattern="^anl-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Id",
        ),
    ]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    model: AnalysisRunItemModel
    """
    Выбранная модель
    """
    retry: AnalysisRunItemRetry
    """
    Повторы обработки
    """
    source: AnalysisRunItemSource
    """
    Источник данных
    """


class AnalysisRunItemResponse(BaseModel):
    """
    Типизированное сообщение AnalysisRunItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    run: AnalysisRunItem
    """
    Типизированное представление ресурса.
    """


class AnalysisRunList(BaseModel):
    """
    Страница анализа с общим числом строк и счётчиками статусов.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    pagination: Pagination
    """
    Метаданные страницы.
    """
    runs: Annotated[list[AnalysisRunDetail], Field(title="Runs")]
    """
    Число запусков.
    """
    statistics: RunStatistics
    """
    Сводные показатели.
    """


class AnalysisScenarioItem(BaseModel):
    """
    Публичное представление сценария анализа.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    active: Annotated[bool, Field(title="Active")]
    """
    Активность.
    """
    analysis: AnalysisScenarioItemAnalysis
    """
    Настройки анализа
    """
    audit: AnalysisScenarioItemAudit
    """
    Сведения о создании и изменении
    """
    description: Annotated[str | None, Field(title="Description")] = None
    """
    Описание.
    """
    id: Annotated[
        str,
        Field(
            pattern="^sca-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            title="Id",
        ),
    ]
    """
    Идентификатор ресурса; существующие префиксы и формат сохраняются.
    """
    name: Annotated[str, Field(title="Name")]
    """
    Название.
    """
    statistics: AnalysisScenarioItemStatistics
    """
    Сводные показатели
    """
    status: Annotated[str, Field(title="Status")]
    """
    Состояние ресурса.
    """
    summary_generation: AnalysisScenarioItemSummaryGeneration
    """
    Настройки формирования резюме
    """
    trigger: AnalysisScenarioItemTrigger
    """
    Условия запуска
    """
    version: Annotated[int, Field(ge=-2147483648, le=2147483647, title="Version")]
    """
    Версия ресурса или схемы.
    """


class AnalysisScenarioItemResponse(BaseModel):
    """
    Типизированное сообщение AnalysisScenarioItemResponse.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    scenario: AnalysisScenarioItem
    """
    Отбор по сценариям.
    """


class AnalysisScenarioList(BaseModel):
    """
    Возвращает серверную страницу сценариев и размер полной выборки.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    pagination: Pagination
    """
    Метаданные страницы.
    """
    scenarios: Annotated[list[AnalysisScenarioItem], Field(title="Scenarios")]
    """
    Типизированная коллекция результатов соответствующего домена.
    """


MetadataGroup.model_rebuild()
