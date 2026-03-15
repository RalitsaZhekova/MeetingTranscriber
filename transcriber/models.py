from django.db import models


class TranscriptJob(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    uploaded_file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    original_filename = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPLOADED,
    )

    error_message = models.TextField(blank=True, null=True)

    transcript_text = models.TextField(blank=True, null=True)

    normalized_audio_file = models.FileField(
        upload_to="processed/audio/%Y/%m/%d/",
        blank=True,
        null=True,
    )

    transcript_json_file = models.FileField(
        upload_to="outputs/json/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    transcript_txt_file = models.FileField(
        upload_to="outputs/txt/%Y/%m/%d/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Job #{self.pk} - {self.original_filename} ({self.status})"

