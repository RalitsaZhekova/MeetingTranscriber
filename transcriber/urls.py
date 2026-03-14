from django.urls import path

from transcriber.views import home, upload_job, job_detail

urlpatterns = [
    path('', home, name='home'),
    path("upload/", upload_job, name="upload_job"),
    path("jobs/<int:pk>/", job_detail, name="job_detail"),
]