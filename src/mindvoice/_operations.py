# Сгенерировано из OpenAPI MindVoice командой uv run python scripts/generate.py.
"""Типизированные операции публичного API MindVoice."""

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

TranscriptFormat = Literal["srt", "vtt", "txt", "txt_timestamps"]


class Client(_SyncClient):
    """Синхронный клиент публичного API MindVoice."""

    def list_workspaces(self) -> models.WorkspaceList:
        """Возвращает пространства, доступные ключу Workspace."""
        return self._json(
            models.WorkspaceList,
            "GET",
            "/v1/workspaces",
        )

    def get_workspace_overview(self, workspace_id: str) -> models.WorkspaceOverview:
        """Возвращает общие сведения о пространстве."""
        return self._json(
            models.WorkspaceOverview,
            "GET",
            "/v1/workspaces/{workspace_id}/overview",
            path={"workspace_id": workspace_id},
        )

    def upload_recording(
        self,
        workspace_id: str,
        *,
        file: BinaryIO,
        filename: str,
        content_type: str,
        metadata: Mapping[str, JsonValue] | None = None,
        recorded_at: datetime | str | None = None,
        retention_days: int | None = None,
        check_duplicates: bool | None = None,
    ) -> models.RecordingItemResponse:
        """Загружает аудиофайл в пространство."""
        return self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings",
            path={"workspace_id": workspace_id},
            upload=_Upload(file, filename, content_type, metadata, recorded_at, retention_days, check_duplicates),
        )

    def list_recordings(
        self,
        workspace_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        uploaded_from: str | None = None,
        uploaded_to: str | None = None,
        recorded_from: str | None = None,
        recorded_to: str | None = None,
        status: Sequence[str] | None = None,
        source: Sequence[str] | None = None,
        search: str | None = None,
        file_id: str | None = None,
        duration_from: int | None = None,
        duration_to: int | None = None,
        size_from: float | None = None,
        size_to: float | None = None,
        silence_ratio_from: float | None = None,
        silence_ratio_to: float | None = None,
        average_loudness_from: float | None = None,
        average_loudness_to: float | None = None,
        peak_from: float | None = None,
        peak_to: float | None = None,
        bitrate_from: int | None = None,
        bitrate_to: int | None = None,
        clipping: Literal["yes", "no", "unknown"] | None = None,
        channels: Sequence[Literal["1", "2", "3+", "unknown"]] | None = None,
        audio_missing: Sequence[Literal["average_loudness", "peak", "silence", "bitrate"]] | None = None,
        transcriptions_count_from: int | None = None,
        transcriptions_count_to: int | None = None,
        analyses_count_from: int | None = None,
        analyses_count_to: int | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
        metadata_filters: Sequence[models.MetadataFilter] | None = None,
        metadata_logic: Literal["and", "or"] | None = None,
        metadata_group: models.MetadataGroup | None = None,
        annulment_status: Literal["not_annulled", "annulled", "all"] | None = None,
        only_without_transcription: bool | None = None,
    ) -> models.RecordingList:
        """Возвращает страницу аудиозаписей."""
        return self._json(
            models.RecordingList,
            "GET",
            "/v1/workspaces/{workspace_id}/recordings",
            path={"workspace_id": workspace_id},
            query={
                "page_size": page_size,
                "offset": offset,
                "uploaded_from": uploaded_from,
                "uploaded_to": uploaded_to,
                "recorded_from": recorded_from,
                "recorded_to": recorded_to,
                "status": status,
                "source": source,
                "search": search,
                "file_id": file_id,
                "duration_from": duration_from,
                "duration_to": duration_to,
                "size_from": size_from,
                "size_to": size_to,
                "silence_ratio_from": silence_ratio_from,
                "silence_ratio_to": silence_ratio_to,
                "average_loudness_from": average_loudness_from,
                "average_loudness_to": average_loudness_to,
                "peak_from": peak_from,
                "peak_to": peak_to,
                "bitrate_from": bitrate_from,
                "bitrate_to": bitrate_to,
                "clipping": clipping,
                "channels": channels,
                "audio_missing": audio_missing,
                "transcriptions_count_from": transcriptions_count_from,
                "transcriptions_count_to": transcriptions_count_to,
                "analyses_count_from": analyses_count_from,
                "analyses_count_to": analyses_count_to,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
                "metadata_logic": metadata_logic,
                "annulment_status": annulment_status,
                "only_without_transcription": only_without_transcription,
            },
            json_query={"metadata_filters": metadata_filters, "metadata_group": metadata_group},
        )

    def import_recording(self, workspace_id: str, body: models.RecordingImport) -> models.RecordingItemResponse:
        """Ставит импорт аудиозаписи по внешней ссылке в очередь."""
        return self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/import",
            path={"workspace_id": workspace_id},
            body=body,
        )

    def retry_recording_import(
        self, workspace_id: str, recording_id: str, body: models.RecordingImportRetry
    ) -> models.RecordingItemResponse:
        """Ставит повторную попытку импорта аудиозаписи в очередь."""
        return self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/import/retry",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            body=body,
        )

    def get_recording(self, workspace_id: str, recording_id: str) -> models.RecordingItemResponse:
        """Возвращает аудиозапись по идентификатору."""
        return self._json(
            models.RecordingItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    def update_recording(self, workspace_id: str, recording_id: str, body: models.RecordingUpdate) -> models.RecordingItemResponse:
        """Изменяет пользовательские поля аудиозаписи по маске."""
        return self._json(
            models.RecordingItemResponse,
            "PATCH",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            body=body,
        )

    def delete_recording(self, workspace_id: str, recording_id: str) -> models.RecordingItemResponse:
        """Удаляет аудиозапись."""
        return self._json(
            models.RecordingItemResponse,
            "DELETE",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    def annul_recording(self, workspace_id: str, recording_id: str) -> models.RecordingItemResponse:
        """Аннулирует аудиозапись."""
        return self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/annul",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    def download_recording(
        self, workspace_id: str, recording_id: str, *, range: str | None = None, if_range: str | None = None
    ) -> AbstractContextManager[httpx.Response]:
        """Возвращает поток исходного аудио."""
        return self._stream(
            "GET",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/download",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            headers={"Range": range, "If-Range": if_range},
        )

    def retry_recording_audio_analysis(self, workspace_id: str, recording_id: str) -> models.RecordingItemResponse:
        """Ставит повторный технический анализ аудиофайла в очередь."""
        return self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/audio-analysis/retry",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    def list_transcription_scenarios(
        self,
        workspace_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        status: Sequence[str] | None = None,
        model: Sequence[str] | None = None,
        trigger_type: Sequence[str] | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
    ) -> models.TranscriptionScenarioList:
        """Возвращает страницу сценариев транскрибации."""
        return self._json(
            models.TranscriptionScenarioList,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-scenarios",
            path={"workspace_id": workspace_id},
            query={
                "page_size": page_size,
                "offset": offset,
                "search": search,
                "status": status,
                "model": model,
                "trigger_type": trigger_type,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
            },
        )

    def get_transcription_scenario(self, workspace_id: str, scenario_id: str) -> models.TranscriptionScenarioItemResponse:
        """Возвращает сценарий транскрибации."""
        return self._json(
            models.TranscriptionScenarioItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-scenarios/{scenario_id}",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
        )

    def set_transcription_scenario_active(
        self, workspace_id: str, scenario_id: str, body: models.ActivationRequest
    ) -> models.TranscriptionScenarioItemResponse:
        """Устанавливает состояние активности сценария транскрибации."""
        return self._json(
            models.TranscriptionScenarioItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-scenarios/{scenario_id}/activation",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            body=body,
        )

    def start_transcription_scenario_execution(
        self, workspace_id: str, scenario_id: str, body: models.TranscriptionScenarioExecutionCreate
    ) -> models.TranscriptionScenarioExecutionItemResponse:
        """Запускает обработку записей по сценарию транскрибации."""
        return self._json(
            models.TranscriptionScenarioExecutionItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-scenarios/{scenario_id}/executions",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            body=body,
        )

    def list_transcription_scenario_executions(
        self,
        workspace_id: str,
        scenario_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        status: Sequence[str] | None = None,
    ) -> models.TranscriptionScenarioExecutionList:
        """Возвращает страницу запусков сценария транскрибации."""
        return self._json(
            models.TranscriptionScenarioExecutionList,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-scenarios/{scenario_id}/executions",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            query={"page_size": page_size, "offset": offset, "status": status},
        )

    def start_transcription_run(
        self, workspace_id: str, recording_id: str, body: models.TranscriptionRunCreate
    ) -> models.TranscriptionRunItemResponse:
        """Запускает транскрибацию аудиозаписи."""
        return self._json(
            models.TranscriptionRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/transcription-runs",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            body=body,
        )

    def list_transcription_runs(
        self,
        workspace_id: str,
        *,
        recording_id: str | None = None,
        job_id: str | UUID | None = None,
        page_size: int | None = None,
        offset: int | None = None,
        transcription_id: str | None = None,
        file_id: str | None = None,
        search: str | None = None,
        status: Sequence[str] | None = None,
        scenario: Sequence[str] | None = None,
        model: Sequence[str] | None = None,
        annulment_status: Literal["not_annulled", "annulled", "all"] | None = None,
        has_summary: bool | None = None,
        has_diarization: bool | None = None,
        include_retried: bool | None = None,
        words_from: int | None = None,
        words_to: int | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
        recorded_from: str | None = None,
        recorded_to: str | None = None,
        metadata_filters: Sequence[models.MetadataFilter] | None = None,
        metadata_logic: Literal["and", "or"] | None = None,
        metadata_group: models.MetadataGroup | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
    ) -> models.TranscriptionRunList:
        """Возвращает страницу запусков транскрибации."""
        return self._json(
            models.TranscriptionRunList,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-runs",
            path={"workspace_id": workspace_id},
            query={
                "recording_id": recording_id,
                "job_id": job_id,
                "page_size": page_size,
                "offset": offset,
                "transcription_id": transcription_id,
                "file_id": file_id,
                "search": search,
                "status": status,
                "scenario": scenario,
                "model": model,
                "annulment_status": annulment_status,
                "has_summary": has_summary,
                "has_diarization": has_diarization,
                "include_retried": include_retried,
                "words_from": words_from,
                "words_to": words_to,
                "created_from": created_from,
                "created_to": created_to,
                "recorded_from": recorded_from,
                "recorded_to": recorded_to,
                "metadata_logic": metadata_logic,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
            },
            json_query={"metadata_filters": metadata_filters, "metadata_group": metadata_group},
        )

    def get_transcription_run(self, workspace_id: str, run_id: str) -> models.TranscriptionRunItemResponse:
        """Возвращает запуск транскрибации по идентификатору."""
        return self._json(
            models.TranscriptionRunItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def get_recording_transcript(self, workspace_id: str, recording_id: str) -> models.TranscriptItemResponse:
        """Возвращает текст расшифровки аудиозаписи."""
        return self._json(
            models.TranscriptItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/transcript",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    def get_transcript(self, workspace_id: str, run_id: str) -> models.TranscriptItemResponse:
        """Возвращает текст расшифровки указанного запуска."""
        return self._json(
            models.TranscriptItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/transcript",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def export_transcript(self, workspace_id: str, run_id: str, *, format: TranscriptFormat) -> AbstractContextManager[httpx.Response]:
        """Возвращает поток файла с текстом расшифровки."""
        return self._stream(
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/transcript/export",
            path={"workspace_id": workspace_id, "run_id": run_id},
            query={"format": format},
        )

    def retry_transcription_run(self, workspace_id: str, run_id: str) -> models.TranscriptionRunItemResponse:
        """Создаёт повторную попытку транскрибации."""
        return self._json(
            models.TranscriptionRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/retry",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def cancel_transcription_run(self, workspace_id: str, run_id: str) -> models.TranscriptionRunItemResponse:
        """Отменяет запуск транскрибации."""
        return self._json(
            models.TranscriptionRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/cancel",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def annul_transcription_run(self, workspace_id: str, run_id: str) -> models.TranscriptionRunItemResponse:
        """Аннулирует запуск транскрибации."""
        return self._json(
            models.TranscriptionRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/annul",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def search_analysis_criteria(
        self, workspace_id: str, *, q: str | None = None, page_size: int | None = None
    ) -> models.AnalysisCriterionSearchResponse:
        """Ищет критерии анализа в пространстве."""
        return self._json(
            models.AnalysisCriterionSearchResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-criteria",
            path={"workspace_id": workspace_id},
            query={"q": q, "page_size": page_size},
        )

    def list_analysis_scenarios(
        self,
        workspace_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        status: Sequence[str] | None = None,
        model: Sequence[str] | None = None,
        trigger_type: Sequence[str] | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
    ) -> models.AnalysisScenarioList:
        """Возвращает страницу сценариев анализа."""
        return self._json(
            models.AnalysisScenarioList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-scenarios",
            path={"workspace_id": workspace_id},
            query={
                "page_size": page_size,
                "offset": offset,
                "search": search,
                "status": status,
                "model": model,
                "trigger_type": trigger_type,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
            },
        )

    def get_analysis_scenario(self, workspace_id: str, scenario_id: str) -> models.AnalysisScenarioItemResponse:
        """Возвращает сценарий анализа."""
        return self._json(
            models.AnalysisScenarioItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-scenarios/{scenario_id}",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
        )

    def set_analysis_scenario_active(
        self, workspace_id: str, scenario_id: str, body: models.ActivationRequest
    ) -> models.AnalysisScenarioItemResponse:
        """Устанавливает состояние активности сценария анализа."""
        return self._json(
            models.AnalysisScenarioItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-scenarios/{scenario_id}/activation",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            body=body,
        )

    def start_analysis_scenario_execution(
        self, workspace_id: str, scenario_id: str, body: models.AnalysisScenarioExecutionCreate
    ) -> models.AnalysisScenarioExecutionItemResponse:
        """Запускает обработку записей по сценарию анализа."""
        return self._json(
            models.AnalysisScenarioExecutionItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-scenarios/{scenario_id}/executions",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            body=body,
        )

    def list_analysis_scenario_executions(
        self,
        workspace_id: str,
        scenario_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        status: Sequence[str] | None = None,
    ) -> models.AnalysisScenarioExecutionList:
        """Возвращает страницу запусков сценария анализа."""
        return self._json(
            models.AnalysisScenarioExecutionList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-scenarios/{scenario_id}/executions",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            query={"page_size": page_size, "offset": offset, "status": status},
        )

    def start_analysis_run(self, workspace_id: str, recording_id: str, body: models.AnalysisRunCreate) -> models.AnalysisRunItemResponse:
        """Запускает анализ аудиозаписи."""
        return self._json(
            models.AnalysisRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/analysis-runs",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            body=body,
        )

    def list_analysis_runs(
        self,
        workspace_id: str,
        *,
        is_test: bool | None = None,
        annulment_status: Literal["not_annulled", "annulled", "all"] | None = None,
        recording_id: str | None = None,
        transcription_run_id: str | None = None,
        execution_id: str | UUID | None = None,
        id: str | None = None,
        file_id: str | None = None,
        transcription_id: str | None = None,
        search: str | None = None,
        status: Sequence[str] | None = None,
        scenario: Sequence[str] | None = None,
        model: Sequence[str | UUID] | None = None,
        transcription_scenario: Sequence[str] | None = None,
        has_summary: bool | None = None,
        flags_from: int | None = None,
        flags_to: int | None = None,
        include_retried: bool | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
        recorded_from: str | None = None,
        recorded_to: str | None = None,
        criterion_id: str | None = None,
        question_op: str | None = None,
        question_value: str | None = None,
        criterion_filters: str | None = None,
        metadata_filters: Sequence[models.MetadataFilter] | None = None,
        metadata_logic: Literal["and", "or"] | None = None,
        metadata_group: models.MetadataGroup | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
        page_size: int | None = None,
        offset: int | None = None,
    ) -> models.AnalysisRunList:
        """Возвращает страницу запусков анализа."""
        return self._json(
            models.AnalysisRunList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-runs",
            path={"workspace_id": workspace_id},
            query={
                "is_test": is_test,
                "annulment_status": annulment_status,
                "recording_id": recording_id,
                "transcription_run_id": transcription_run_id,
                "execution_id": execution_id,
                "id": id,
                "file_id": file_id,
                "transcription_id": transcription_id,
                "search": search,
                "status": status,
                "scenario": scenario,
                "model": model,
                "transcription_scenario": transcription_scenario,
                "has_summary": has_summary,
                "flags_from": flags_from,
                "flags_to": flags_to,
                "include_retried": include_retried,
                "created_from": created_from,
                "created_to": created_to,
                "recorded_from": recorded_from,
                "recorded_to": recorded_to,
                "criterion_id": criterion_id,
                "question_op": question_op,
                "question_value": question_value,
                "criterion_filters": criterion_filters,
                "metadata_logic": metadata_logic,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
                "page_size": page_size,
                "offset": offset,
            },
            json_query={"metadata_filters": metadata_filters, "metadata_group": metadata_group},
        )

    def get_analysis_run(self, workspace_id: str, run_id: str) -> models.AnalysisRunDetailResponse:
        """Возвращает подробности запуска анализа."""
        return self._json(
            models.AnalysisRunDetailResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-runs/{run_id}",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def get_analysis_result(self, workspace_id: str, result_id: str | UUID) -> models.AnalysisRunDetailResponse:
        """Возвращает результат анализа по идентификатору результата."""
        return self._json(
            models.AnalysisRunDetailResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-results/{result_id}",
            path={"workspace_id": workspace_id, "result_id": result_id},
        )

    def retry_analysis_run(self, workspace_id: str, run_id: str) -> models.AnalysisRunDetailResponse:
        """Создаёт повторную попытку анализа."""
        return self._json(
            models.AnalysisRunDetailResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-runs/{run_id}/retry",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def annul_analysis_run(self, workspace_id: str, run_id: str) -> models.AnalysisRunDetailResponse:
        """Аннулирует запуск анализа."""
        return self._json(
            models.AnalysisRunDetailResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-runs/{run_id}/annul",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def cancel_analysis_run(self, workspace_id: str, run_id: str) -> models.AnalysisRunDetailResponse:
        """Отменяет запуск анализа."""
        return self._json(
            models.AnalysisRunDetailResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-runs/{run_id}/cancel",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def get_recording_analysis_result(
        self, workspace_id: str, recording_id: str, analysis_run_id: str, *, include_recording: bool | None = None
    ) -> models.AnalysisResultItemResponse:
        """Возвращает результат указанного запуска для аудиозаписи."""
        return self._json(
            models.AnalysisResultItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/analysis-results/{analysis_run_id}",
            path={"workspace_id": workspace_id, "recording_id": recording_id, "analysis_run_id": analysis_run_id},
            query={"include_recording": include_recording},
        )

    def list_analysis_results(
        self,
        workspace_id: str,
        *,
        recording_id: str | None = None,
        annulment_status: Literal["not_annulled", "annulled", "all"] | None = None,
        transcription_run_id: str | None = None,
        analysis_scenario_id: str | None = None,
        include_recording: bool | None = None,
        page_size: int | None = None,
        offset: int | None = None,
    ) -> models.AnalysisResultList:
        """Возвращает страницу результатов анализа."""
        return self._json(
            models.AnalysisResultList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-results",
            path={"workspace_id": workspace_id},
            query={
                "recording_id": recording_id,
                "annulment_status": annulment_status,
                "transcription_run_id": transcription_run_id,
                "analysis_scenario_id": analysis_scenario_id,
                "include_recording": include_recording,
                "page_size": page_size,
                "offset": offset,
            },
        )

    def list_analysis_criterion_templates(
        self, workspace_id: str, *, locale: str | None = None, category: str | None = None
    ) -> models.AnalysisTemplateList:
        """Возвращает каталог шаблонов критериев анализа."""
        return self._json(
            models.AnalysisTemplateList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-criterion-templates",
            path={"workspace_id": workspace_id},
            query={"locale": locale, "category": category},
        )

    def get_analysis_criterion_template_version(
        self, workspace_id: str, template_id: str, version: int, *, locale: str | None = None
    ) -> models.AnalysisTemplateItemResponse:
        """Возвращает указанную редакцию шаблона критерия анализа."""
        return self._json(
            models.AnalysisTemplateItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-criterion-templates/{template_id}/versions/{version}",
            path={"workspace_id": workspace_id, "template_id": template_id, "version": version},
            query={"locale": locale},
        )


class AsyncClient(_AsyncClient):
    """Асинхронный клиент публичного API MindVoice."""

    async def list_workspaces(self) -> models.WorkspaceList:
        """Возвращает пространства, доступные ключу Workspace."""
        return await self._json(
            models.WorkspaceList,
            "GET",
            "/v1/workspaces",
        )

    async def get_workspace_overview(self, workspace_id: str) -> models.WorkspaceOverview:
        """Возвращает общие сведения о пространстве."""
        return await self._json(
            models.WorkspaceOverview,
            "GET",
            "/v1/workspaces/{workspace_id}/overview",
            path={"workspace_id": workspace_id},
        )

    async def upload_recording(
        self,
        workspace_id: str,
        *,
        file: BinaryIO,
        filename: str,
        content_type: str,
        metadata: Mapping[str, JsonValue] | None = None,
        recorded_at: datetime | str | None = None,
        retention_days: int | None = None,
        check_duplicates: bool | None = None,
    ) -> models.RecordingItemResponse:
        """Загружает аудиофайл в пространство."""
        return await self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings",
            path={"workspace_id": workspace_id},
            upload=_Upload(file, filename, content_type, metadata, recorded_at, retention_days, check_duplicates),
        )

    async def list_recordings(
        self,
        workspace_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        uploaded_from: str | None = None,
        uploaded_to: str | None = None,
        recorded_from: str | None = None,
        recorded_to: str | None = None,
        status: Sequence[str] | None = None,
        source: Sequence[str] | None = None,
        search: str | None = None,
        file_id: str | None = None,
        duration_from: int | None = None,
        duration_to: int | None = None,
        size_from: float | None = None,
        size_to: float | None = None,
        silence_ratio_from: float | None = None,
        silence_ratio_to: float | None = None,
        average_loudness_from: float | None = None,
        average_loudness_to: float | None = None,
        peak_from: float | None = None,
        peak_to: float | None = None,
        bitrate_from: int | None = None,
        bitrate_to: int | None = None,
        clipping: Literal["yes", "no", "unknown"] | None = None,
        channels: Sequence[Literal["1", "2", "3+", "unknown"]] | None = None,
        audio_missing: Sequence[Literal["average_loudness", "peak", "silence", "bitrate"]] | None = None,
        transcriptions_count_from: int | None = None,
        transcriptions_count_to: int | None = None,
        analyses_count_from: int | None = None,
        analyses_count_to: int | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
        metadata_filters: Sequence[models.MetadataFilter] | None = None,
        metadata_logic: Literal["and", "or"] | None = None,
        metadata_group: models.MetadataGroup | None = None,
        annulment_status: Literal["not_annulled", "annulled", "all"] | None = None,
        only_without_transcription: bool | None = None,
    ) -> models.RecordingList:
        """Возвращает страницу аудиозаписей."""
        return await self._json(
            models.RecordingList,
            "GET",
            "/v1/workspaces/{workspace_id}/recordings",
            path={"workspace_id": workspace_id},
            query={
                "page_size": page_size,
                "offset": offset,
                "uploaded_from": uploaded_from,
                "uploaded_to": uploaded_to,
                "recorded_from": recorded_from,
                "recorded_to": recorded_to,
                "status": status,
                "source": source,
                "search": search,
                "file_id": file_id,
                "duration_from": duration_from,
                "duration_to": duration_to,
                "size_from": size_from,
                "size_to": size_to,
                "silence_ratio_from": silence_ratio_from,
                "silence_ratio_to": silence_ratio_to,
                "average_loudness_from": average_loudness_from,
                "average_loudness_to": average_loudness_to,
                "peak_from": peak_from,
                "peak_to": peak_to,
                "bitrate_from": bitrate_from,
                "bitrate_to": bitrate_to,
                "clipping": clipping,
                "channels": channels,
                "audio_missing": audio_missing,
                "transcriptions_count_from": transcriptions_count_from,
                "transcriptions_count_to": transcriptions_count_to,
                "analyses_count_from": analyses_count_from,
                "analyses_count_to": analyses_count_to,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
                "metadata_logic": metadata_logic,
                "annulment_status": annulment_status,
                "only_without_transcription": only_without_transcription,
            },
            json_query={"metadata_filters": metadata_filters, "metadata_group": metadata_group},
        )

    async def import_recording(self, workspace_id: str, body: models.RecordingImport) -> models.RecordingItemResponse:
        """Ставит импорт аудиозаписи по внешней ссылке в очередь."""
        return await self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/import",
            path={"workspace_id": workspace_id},
            body=body,
        )

    async def retry_recording_import(
        self, workspace_id: str, recording_id: str, body: models.RecordingImportRetry
    ) -> models.RecordingItemResponse:
        """Ставит повторную попытку импорта аудиозаписи в очередь."""
        return await self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/import/retry",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            body=body,
        )

    async def get_recording(self, workspace_id: str, recording_id: str) -> models.RecordingItemResponse:
        """Возвращает аудиозапись по идентификатору."""
        return await self._json(
            models.RecordingItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    async def update_recording(self, workspace_id: str, recording_id: str, body: models.RecordingUpdate) -> models.RecordingItemResponse:
        """Изменяет пользовательские поля аудиозаписи по маске."""
        return await self._json(
            models.RecordingItemResponse,
            "PATCH",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            body=body,
        )

    async def delete_recording(self, workspace_id: str, recording_id: str) -> models.RecordingItemResponse:
        """Удаляет аудиозапись."""
        return await self._json(
            models.RecordingItemResponse,
            "DELETE",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    async def annul_recording(self, workspace_id: str, recording_id: str) -> models.RecordingItemResponse:
        """Аннулирует аудиозапись."""
        return await self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/annul",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    def download_recording(
        self, workspace_id: str, recording_id: str, *, range: str | None = None, if_range: str | None = None
    ) -> AbstractAsyncContextManager[httpx.Response]:
        """Возвращает поток исходного аудио."""
        return self._stream(
            "GET",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/download",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            headers={"Range": range, "If-Range": if_range},
        )

    async def retry_recording_audio_analysis(self, workspace_id: str, recording_id: str) -> models.RecordingItemResponse:
        """Ставит повторный технический анализ аудиофайла в очередь."""
        return await self._json(
            models.RecordingItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/audio-analysis/retry",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    async def list_transcription_scenarios(
        self,
        workspace_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        status: Sequence[str] | None = None,
        model: Sequence[str] | None = None,
        trigger_type: Sequence[str] | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
    ) -> models.TranscriptionScenarioList:
        """Возвращает страницу сценариев транскрибации."""
        return await self._json(
            models.TranscriptionScenarioList,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-scenarios",
            path={"workspace_id": workspace_id},
            query={
                "page_size": page_size,
                "offset": offset,
                "search": search,
                "status": status,
                "model": model,
                "trigger_type": trigger_type,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
            },
        )

    async def get_transcription_scenario(self, workspace_id: str, scenario_id: str) -> models.TranscriptionScenarioItemResponse:
        """Возвращает сценарий транскрибации."""
        return await self._json(
            models.TranscriptionScenarioItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-scenarios/{scenario_id}",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
        )

    async def set_transcription_scenario_active(
        self, workspace_id: str, scenario_id: str, body: models.ActivationRequest
    ) -> models.TranscriptionScenarioItemResponse:
        """Устанавливает состояние активности сценария транскрибации."""
        return await self._json(
            models.TranscriptionScenarioItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-scenarios/{scenario_id}/activation",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            body=body,
        )

    async def start_transcription_scenario_execution(
        self, workspace_id: str, scenario_id: str, body: models.TranscriptionScenarioExecutionCreate
    ) -> models.TranscriptionScenarioExecutionItemResponse:
        """Запускает обработку записей по сценарию транскрибации."""
        return await self._json(
            models.TranscriptionScenarioExecutionItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-scenarios/{scenario_id}/executions",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            body=body,
        )

    async def list_transcription_scenario_executions(
        self,
        workspace_id: str,
        scenario_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        status: Sequence[str] | None = None,
    ) -> models.TranscriptionScenarioExecutionList:
        """Возвращает страницу запусков сценария транскрибации."""
        return await self._json(
            models.TranscriptionScenarioExecutionList,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-scenarios/{scenario_id}/executions",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            query={"page_size": page_size, "offset": offset, "status": status},
        )

    async def start_transcription_run(
        self, workspace_id: str, recording_id: str, body: models.TranscriptionRunCreate
    ) -> models.TranscriptionRunItemResponse:
        """Запускает транскрибацию аудиозаписи."""
        return await self._json(
            models.TranscriptionRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/transcription-runs",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            body=body,
        )

    async def list_transcription_runs(
        self,
        workspace_id: str,
        *,
        recording_id: str | None = None,
        job_id: str | UUID | None = None,
        page_size: int | None = None,
        offset: int | None = None,
        transcription_id: str | None = None,
        file_id: str | None = None,
        search: str | None = None,
        status: Sequence[str] | None = None,
        scenario: Sequence[str] | None = None,
        model: Sequence[str] | None = None,
        annulment_status: Literal["not_annulled", "annulled", "all"] | None = None,
        has_summary: bool | None = None,
        has_diarization: bool | None = None,
        include_retried: bool | None = None,
        words_from: int | None = None,
        words_to: int | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
        recorded_from: str | None = None,
        recorded_to: str | None = None,
        metadata_filters: Sequence[models.MetadataFilter] | None = None,
        metadata_logic: Literal["and", "or"] | None = None,
        metadata_group: models.MetadataGroup | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
    ) -> models.TranscriptionRunList:
        """Возвращает страницу запусков транскрибации."""
        return await self._json(
            models.TranscriptionRunList,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-runs",
            path={"workspace_id": workspace_id},
            query={
                "recording_id": recording_id,
                "job_id": job_id,
                "page_size": page_size,
                "offset": offset,
                "transcription_id": transcription_id,
                "file_id": file_id,
                "search": search,
                "status": status,
                "scenario": scenario,
                "model": model,
                "annulment_status": annulment_status,
                "has_summary": has_summary,
                "has_diarization": has_diarization,
                "include_retried": include_retried,
                "words_from": words_from,
                "words_to": words_to,
                "created_from": created_from,
                "created_to": created_to,
                "recorded_from": recorded_from,
                "recorded_to": recorded_to,
                "metadata_logic": metadata_logic,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
            },
            json_query={"metadata_filters": metadata_filters, "metadata_group": metadata_group},
        )

    async def get_transcription_run(self, workspace_id: str, run_id: str) -> models.TranscriptionRunItemResponse:
        """Возвращает запуск транскрибации по идентификатору."""
        return await self._json(
            models.TranscriptionRunItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    async def get_recording_transcript(self, workspace_id: str, recording_id: str) -> models.TranscriptItemResponse:
        """Возвращает текст расшифровки аудиозаписи."""
        return await self._json(
            models.TranscriptItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/transcript",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
        )

    async def get_transcript(self, workspace_id: str, run_id: str) -> models.TranscriptItemResponse:
        """Возвращает текст расшифровки указанного запуска."""
        return await self._json(
            models.TranscriptItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/transcript",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    def export_transcript(self, workspace_id: str, run_id: str, *, format: TranscriptFormat) -> AbstractAsyncContextManager[httpx.Response]:
        """Возвращает поток файла с текстом расшифровки."""
        return self._stream(
            "GET",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/transcript/export",
            path={"workspace_id": workspace_id, "run_id": run_id},
            query={"format": format},
        )

    async def retry_transcription_run(self, workspace_id: str, run_id: str) -> models.TranscriptionRunItemResponse:
        """Создаёт повторную попытку транскрибации."""
        return await self._json(
            models.TranscriptionRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/retry",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    async def cancel_transcription_run(self, workspace_id: str, run_id: str) -> models.TranscriptionRunItemResponse:
        """Отменяет запуск транскрибации."""
        return await self._json(
            models.TranscriptionRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/cancel",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    async def annul_transcription_run(self, workspace_id: str, run_id: str) -> models.TranscriptionRunItemResponse:
        """Аннулирует запуск транскрибации."""
        return await self._json(
            models.TranscriptionRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/transcription-runs/{run_id}/annul",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    async def search_analysis_criteria(
        self, workspace_id: str, *, q: str | None = None, page_size: int | None = None
    ) -> models.AnalysisCriterionSearchResponse:
        """Ищет критерии анализа в пространстве."""
        return await self._json(
            models.AnalysisCriterionSearchResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-criteria",
            path={"workspace_id": workspace_id},
            query={"q": q, "page_size": page_size},
        )

    async def list_analysis_scenarios(
        self,
        workspace_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        status: Sequence[str] | None = None,
        model: Sequence[str] | None = None,
        trigger_type: Sequence[str] | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
    ) -> models.AnalysisScenarioList:
        """Возвращает страницу сценариев анализа."""
        return await self._json(
            models.AnalysisScenarioList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-scenarios",
            path={"workspace_id": workspace_id},
            query={
                "page_size": page_size,
                "offset": offset,
                "search": search,
                "status": status,
                "model": model,
                "trigger_type": trigger_type,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
            },
        )

    async def get_analysis_scenario(self, workspace_id: str, scenario_id: str) -> models.AnalysisScenarioItemResponse:
        """Возвращает сценарий анализа."""
        return await self._json(
            models.AnalysisScenarioItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-scenarios/{scenario_id}",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
        )

    async def set_analysis_scenario_active(
        self, workspace_id: str, scenario_id: str, body: models.ActivationRequest
    ) -> models.AnalysisScenarioItemResponse:
        """Устанавливает состояние активности сценария анализа."""
        return await self._json(
            models.AnalysisScenarioItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-scenarios/{scenario_id}/activation",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            body=body,
        )

    async def start_analysis_scenario_execution(
        self, workspace_id: str, scenario_id: str, body: models.AnalysisScenarioExecutionCreate
    ) -> models.AnalysisScenarioExecutionItemResponse:
        """Запускает обработку записей по сценарию анализа."""
        return await self._json(
            models.AnalysisScenarioExecutionItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-scenarios/{scenario_id}/executions",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            body=body,
        )

    async def list_analysis_scenario_executions(
        self,
        workspace_id: str,
        scenario_id: str,
        *,
        page_size: int | None = None,
        offset: int | None = None,
        status: Sequence[str] | None = None,
    ) -> models.AnalysisScenarioExecutionList:
        """Возвращает страницу запусков сценария анализа."""
        return await self._json(
            models.AnalysisScenarioExecutionList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-scenarios/{scenario_id}/executions",
            path={"workspace_id": workspace_id, "scenario_id": scenario_id},
            query={"page_size": page_size, "offset": offset, "status": status},
        )

    async def start_analysis_run(
        self, workspace_id: str, recording_id: str, body: models.AnalysisRunCreate
    ) -> models.AnalysisRunItemResponse:
        """Запускает анализ аудиозаписи."""
        return await self._json(
            models.AnalysisRunItemResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/analysis-runs",
            path={"workspace_id": workspace_id, "recording_id": recording_id},
            body=body,
        )

    async def list_analysis_runs(
        self,
        workspace_id: str,
        *,
        is_test: bool | None = None,
        annulment_status: Literal["not_annulled", "annulled", "all"] | None = None,
        recording_id: str | None = None,
        transcription_run_id: str | None = None,
        execution_id: str | UUID | None = None,
        id: str | None = None,
        file_id: str | None = None,
        transcription_id: str | None = None,
        search: str | None = None,
        status: Sequence[str] | None = None,
        scenario: Sequence[str] | None = None,
        model: Sequence[str | UUID] | None = None,
        transcription_scenario: Sequence[str] | None = None,
        has_summary: bool | None = None,
        flags_from: int | None = None,
        flags_to: int | None = None,
        include_retried: bool | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
        recorded_from: str | None = None,
        recorded_to: str | None = None,
        criterion_id: str | None = None,
        question_op: str | None = None,
        question_value: str | None = None,
        criterion_filters: str | None = None,
        metadata_filters: Sequence[models.MetadataFilter] | None = None,
        metadata_logic: Literal["and", "or"] | None = None,
        metadata_group: models.MetadataGroup | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
        page_size: int | None = None,
        offset: int | None = None,
    ) -> models.AnalysisRunList:
        """Возвращает страницу запусков анализа."""
        return await self._json(
            models.AnalysisRunList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-runs",
            path={"workspace_id": workspace_id},
            query={
                "is_test": is_test,
                "annulment_status": annulment_status,
                "recording_id": recording_id,
                "transcription_run_id": transcription_run_id,
                "execution_id": execution_id,
                "id": id,
                "file_id": file_id,
                "transcription_id": transcription_id,
                "search": search,
                "status": status,
                "scenario": scenario,
                "model": model,
                "transcription_scenario": transcription_scenario,
                "has_summary": has_summary,
                "flags_from": flags_from,
                "flags_to": flags_to,
                "include_retried": include_retried,
                "created_from": created_from,
                "created_to": created_to,
                "recorded_from": recorded_from,
                "recorded_to": recorded_to,
                "criterion_id": criterion_id,
                "question_op": question_op,
                "question_value": question_value,
                "criterion_filters": criterion_filters,
                "metadata_logic": metadata_logic,
                "sort_by": sort_by,
                "sort_direction": sort_direction,
                "page_size": page_size,
                "offset": offset,
            },
            json_query={"metadata_filters": metadata_filters, "metadata_group": metadata_group},
        )

    async def get_analysis_run(self, workspace_id: str, run_id: str) -> models.AnalysisRunDetailResponse:
        """Возвращает подробности запуска анализа."""
        return await self._json(
            models.AnalysisRunDetailResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-runs/{run_id}",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    async def get_analysis_result(self, workspace_id: str, result_id: str | UUID) -> models.AnalysisRunDetailResponse:
        """Возвращает результат анализа по идентификатору результата."""
        return await self._json(
            models.AnalysisRunDetailResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-results/{result_id}",
            path={"workspace_id": workspace_id, "result_id": result_id},
        )

    async def retry_analysis_run(self, workspace_id: str, run_id: str) -> models.AnalysisRunDetailResponse:
        """Создаёт повторную попытку анализа."""
        return await self._json(
            models.AnalysisRunDetailResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-runs/{run_id}/retry",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    async def annul_analysis_run(self, workspace_id: str, run_id: str) -> models.AnalysisRunDetailResponse:
        """Аннулирует запуск анализа."""
        return await self._json(
            models.AnalysisRunDetailResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-runs/{run_id}/annul",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    async def cancel_analysis_run(self, workspace_id: str, run_id: str) -> models.AnalysisRunDetailResponse:
        """Отменяет запуск анализа."""
        return await self._json(
            models.AnalysisRunDetailResponse,
            "POST",
            "/v1/workspaces/{workspace_id}/analysis-runs/{run_id}/cancel",
            path={"workspace_id": workspace_id, "run_id": run_id},
        )

    async def get_recording_analysis_result(
        self, workspace_id: str, recording_id: str, analysis_run_id: str, *, include_recording: bool | None = None
    ) -> models.AnalysisResultItemResponse:
        """Возвращает результат указанного запуска для аудиозаписи."""
        return await self._json(
            models.AnalysisResultItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/recordings/{recording_id}/analysis-results/{analysis_run_id}",
            path={"workspace_id": workspace_id, "recording_id": recording_id, "analysis_run_id": analysis_run_id},
            query={"include_recording": include_recording},
        )

    async def list_analysis_results(
        self,
        workspace_id: str,
        *,
        recording_id: str | None = None,
        annulment_status: Literal["not_annulled", "annulled", "all"] | None = None,
        transcription_run_id: str | None = None,
        analysis_scenario_id: str | None = None,
        include_recording: bool | None = None,
        page_size: int | None = None,
        offset: int | None = None,
    ) -> models.AnalysisResultList:
        """Возвращает страницу результатов анализа."""
        return await self._json(
            models.AnalysisResultList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-results",
            path={"workspace_id": workspace_id},
            query={
                "recording_id": recording_id,
                "annulment_status": annulment_status,
                "transcription_run_id": transcription_run_id,
                "analysis_scenario_id": analysis_scenario_id,
                "include_recording": include_recording,
                "page_size": page_size,
                "offset": offset,
            },
        )

    async def list_analysis_criterion_templates(
        self, workspace_id: str, *, locale: str | None = None, category: str | None = None
    ) -> models.AnalysisTemplateList:
        """Возвращает каталог шаблонов критериев анализа."""
        return await self._json(
            models.AnalysisTemplateList,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-criterion-templates",
            path={"workspace_id": workspace_id},
            query={"locale": locale, "category": category},
        )

    async def get_analysis_criterion_template_version(
        self, workspace_id: str, template_id: str, version: int, *, locale: str | None = None
    ) -> models.AnalysisTemplateItemResponse:
        """Возвращает указанную редакцию шаблона критерия анализа."""
        return await self._json(
            models.AnalysisTemplateItemResponse,
            "GET",
            "/v1/workspaces/{workspace_id}/analysis-criterion-templates/{template_id}/versions/{version}",
            path={"workspace_id": workspace_id, "template_id": template_id, "version": version},
            query={"locale": locale},
        )
