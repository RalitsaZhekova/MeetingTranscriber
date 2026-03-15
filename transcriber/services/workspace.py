from pathlib import Path

from django.conf import settings


def get_job_temp_dir(job_id: int) -> Path:
    temp_dir = Path(settings.MEDIA_ROOT) / "temp" / "jobs" / str(job_id)
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir
