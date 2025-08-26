from django import forms
from .models import Document
from pathlib import Path

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "author", "uploaded_file", "formatted_text"]

    def clean_uploaded_file(self):
        f = self.cleaned_data.get("uploaded_file")
        if not f:
            return f
        ext = Path(f.name).suffix.lower()
        if ext not in [".docx"]:
            raise forms.ValidationError("Please upload a .docx file for best formatting preservation.")
        return f
