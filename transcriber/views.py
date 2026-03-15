from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from transcriber.forms import TranscriptJobForm
from transcriber.models import TranscriptJob
from .tasks import test_task

# Create your views here.
def home(request):
    return render(request, "transcriber/index.html")


def upload_job(request):
    if request.method == "POST":
        form = TranscriptJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()
            return redirect("job_detail", pk=job.pk)
    else:
        form = TranscriptJobForm()

    return render(request, "transcriber/upload.html", {"form": form})


def job_detail(request, pk):
    job = get_object_or_404(TranscriptJob, pk=pk)
    return render(request, "transcriber/job_detail.html", {"job": job})


def trigger_test_task(request):
    task = test_task.delay()
    return render(
        request,
        "transcriber/task_triggered.html",
        {"task_id": task.id},
    )
