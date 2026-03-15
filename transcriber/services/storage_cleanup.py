from transcriber.models import TranscriptJob


def delete_job_files(job: TranscriptJob) -> None:
    file_fields = [
        "uploaded_file",
        "normalized_audio_file",
        "transcript_json_file",
        "transcript_txt_file",
    ]

    for field_name in file_fields:
        field = getattr(job, field_name, None)
        if field and field.name:
            try:
                field.delete(save=False)
            except Exception:
                pass
