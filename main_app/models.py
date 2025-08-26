from django.db import models
from ckeditor.fields import RichTextField
import re

class Document(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    uploaded_file = models.FileField(upload_to="uploads/", blank=True, null=True)
    formatted_text = RichTextField(blank=True, null=True)

    # Counts
    word_count = models.PositiveIntegerField(default=0)
    char_count = models.PositiveIntegerField(default=0)
    sentence_count = models.PositiveIntegerField(default=0)
    line_count = models.PositiveIntegerField(default=0)
    paragraph_count = models.PositiveIntegerField(default=0)

    # Slug & timestamps
    slug = models.SlugField(unique=True, blank=True)  # URL-safe identifier
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def camel_case(self, s):
        s = re.sub(r"[^a-zA-Z0-9 ]+", "", s)  # remove non-alphanum chars
        parts = s.split()
        return "".join(word.capitalize() for word in parts)

    def generate_slug(self):
        title_part = self.camel_case(self.title)
        author_part = self.camel_case(self.author)
        return f"{title_part}_{author_part}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = self.generate_slug()
            slug = base_slug
            counter = 1
            while Document.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}_{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
