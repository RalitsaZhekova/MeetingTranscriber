from django.urls import path

from transcriber.views import home

urlpatterns = [
    path('', home, name='home'),
]