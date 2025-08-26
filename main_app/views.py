from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DocumentForm
from .models import Document
from .utils import process_docx


# Home view
def home(request):
    return render(request, "home.html")


# List all "pieces"
def pieces_index(request):
    pieces = Document.objects.all().order_by("-created_at")
    return render(request, "pieces/index.html", {"pieces": pieces})


def uploader(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)

            # Generate slug and check duplicates
            slug = doc.generate_slug()
            if Document.objects.filter(slug=slug).exists():
                messages.error(
                    request,
                    "A piece with this Title + Author already exists. Please choose a different title.",
                )
                return render(request, "uploader.html", {"form": form})

            doc.slug = slug
            doc.save()  # Save so file exists on disk

            # Convert + count stats
            if doc.uploaded_file:
                try:
                    (
                        html_content,
                        word_count,
                        char_count,
                        sentence_count,
                        line_count,
                        paragraph_count,
                    ) = process_docx(doc.uploaded_file.path)

                    doc.formatted_text = html_content
                    doc.word_count = word_count
                    doc.char_count = char_count
                    doc.sentence_count = sentence_count
                    doc.line_count = line_count
                    doc.paragraph_count = paragraph_count

                except Exception as e:
                    messages.error(request, f"Could not process file: {e}")
                    return render(request, "uploader.html", {"form": form})

            doc.save()
            return redirect("document_detail", slug=doc.slug)
    else:
        form = DocumentForm()

    return render(request, "uploader.html", {"form": form})


def document_detail(request, slug):
    document = get_object_or_404(Document, slug=slug)
    return render(request, "pieces/detail.html", {"document": document})
