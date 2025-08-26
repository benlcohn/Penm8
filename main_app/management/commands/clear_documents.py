from django.core.management.base import BaseCommand
from main_app.models import Document
import os

class Command(BaseCommand):
    help = "Delete all Document objects and their uploaded files (reset pieces)."

    def handle(self, *args, **kwargs):
        deleted_files = 0
        for doc in Document.objects.all():
            if doc.uploaded_file and doc.uploaded_file.path:
                try:
                    os.remove(doc.uploaded_file.path)
                    deleted_files += 1
                except FileNotFoundError:
                    pass  # already gone
            doc.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {deleted_files} files and all Document records."
            )
        )


## python manage.py clear_documents to run