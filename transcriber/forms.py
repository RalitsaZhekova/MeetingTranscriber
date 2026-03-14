from django import forms

from .models import TranscriptJob


class TranscriptJobForm(forms.ModelForm):
    class Meta:
        model = TranscriptJob
        fields = ["uploaded_file"]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get("uploaded_file"):
            instance.original_filename = self.cleaned_data["uploaded_file"].name

        if commit:
            instance.save()

        return instance
