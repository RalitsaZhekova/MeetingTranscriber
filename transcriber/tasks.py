import time
from pathlib import Path

from celery import shared_task
from django.core.files import File

from transcriber.models import TranscriptJob
from transcriber.services.media import normalize_audio_to_wav


@shared_task
def test_task():
    time.sleep(5)
    return "Celery is working"

@shared_task
def process_uploaded_media(job_id: int):
    job = TranscriptJob.objects.get(pk=job_id)

    try:
        job.status = TranscriptJob.Status.PROCESSING
        job.error_message = ""
        job.save(update_fields=["status", "error_message", "updated_at"])

        input_path = Path(job.uploaded_file.path)
        temp_output_path = input_path.parent / f"{input_path.stem}.normalized.wav"

        normalized_path = normalize_audio_to_wav(input_path, temp_output_path)

        with normalized_path.open("rb") as f:
            job.normalized_audio_file.save(
                f"{input_path.stem}.normalized.wav",
                File(f),
                save=False,
            )

        job.save(update_fields=["normalized_audio_file", "updated_at"])

    except Exception as exc:
        job.status = TranscriptJob.Status.FAILED
        job.error_message = str(exc)
        job.save(update_fields=["status", "error_message", "updated_at"])
        raise