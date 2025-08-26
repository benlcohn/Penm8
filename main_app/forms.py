from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Document
from pathlib import Path

class DocumentForm(forms.ModelForm):
    formatted_text = forms.CharField(widget=CKEditorWidget(config_name='default'), required=False)

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
