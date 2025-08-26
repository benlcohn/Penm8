from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "word_count", "char_count")
    search_fields = ("title", "author")
    readonly_fields = ("formatted_text",)  # so you can *see* the HTML
