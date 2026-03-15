import time
from pathlib import Path

from celery import shared_task
from django.core.files import File

from transcriber.models import TranscriptJob
from transcriber.services.cleanup import safe_rmtree
from transcriber.services.media import normalize_audio_to_wav
from transcriber.services.transcription import transcribe_audio, save_transcript_json
from transcriber.services.workspace import get_job_temp_dir


@shared_task
def test_task():
    time.sleep(5)
    return "Celery is working"

@shared_task
def process_uploaded_media(job_id: int):
    job = TranscriptJob.objects.get(pk=job_id)
    temp_dir = None

    try:
        job.status = TranscriptJob.Status.PROCESSING
        job.error_message = ""
        job.save(update_fields=["status", "error_message", "updated_at"])

        input_path = Path(job.uploaded_file.path)
        temp_dir = get_job_temp_dir(job.id)

        normalized_path = temp_dir / "normalized.wav"
        temp_json_path = temp_dir / "transcript.json"
        temp_txt_path = temp_dir / "transcript.txt"

        normalize_audio_to_wav(input_path, normalized_path)

        with normalized_path.open("rb") as f:
            job.normalized_audio_file.save(
                f"{input_path.stem}.normalized.wav",
                File(f),
                save=False,
            )

        job.save(update_fields=["normalized_audio_file", "updated_at"])

        selected_language = (
            None
            if job.selected_language == TranscriptJob.LanguageChoice.AUTO
            else job.selected_language
        )

        transcription_result = transcribe_audio(
            normalized_path,
            model_size="medium",
            language=selected_language,
        )

        save_transcript_json(temp_json_path, transcription_result)

        temp_txt_path.write_text(
            transcription_result["transcript_text"],
            encoding="utf-8",
        )

        with temp_json_path.open("rb") as f:
            job.transcript_json_file.save(
                f"{input_path.stem}.transcript.json",
                File(f),
                save=False,
            )

        with temp_txt_path.open("rb") as f:
            job.transcript_txt_file.save(
                f"{input_path.stem}.transcript.txt",
                File(f),
                save=False,
            )

        job.transcript_text = transcription_result["transcript_text"]
        job.status = TranscriptJob.Status.COMPLETED
        job.save(
            update_fields=[
                "transcript_json_file",
                "transcript_txt_file",
                "transcript_text",
                "status",
                "updated_at",
            ]
        )

    except Exception as exc:
        job.status = TranscriptJob.Status.FAILED
        job.error_message = str(exc)
        job.save(update_fields=["status", "error_message", "updated_at"])
        raise

    finally:
        if temp_dir is not None:
            safe_rmtree(temp_dir)