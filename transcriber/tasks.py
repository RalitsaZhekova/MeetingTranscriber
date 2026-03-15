import time

from celery import shared_task


@shared_task
def test_task():
    time.sleep(5)
    return "Celery is working"