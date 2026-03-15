import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meeting_transcriber.settings")

app = Celery("meeting_transcriber")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
