from django.contrib import admin

from .models import TranscriptJob


@admin.register(TranscriptJob)
class TranscriptJobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "original_filename",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("original_filename", "error_message", "transcript_text")
    readonly_fields = ("created_at", "updated_at")

