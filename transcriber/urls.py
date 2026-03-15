from django.urls import path

from transcriber.views import home, upload_job, job_detail, trigger_test_task

urlpatterns = [
    path('', home, name='home'),
    path("upload/", upload_job, name="upload_job"),
    path("jobs/<int:pk>/", job_detail, name="job_detail"),
    path("test-task/", trigger_test_task, name="trigger_test_task"),
]