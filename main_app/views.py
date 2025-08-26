from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DocumentForm
from .models import Document
from .utils import (
    process_docx,
    process_docx_perline,
    process_html,
    process_html_perline,
)


# Home view
def home(request):
    return render(request, "home.html")


# List all "pieces"
def pieces_index(request):
    pieces = Document.objects.all().order_by("-created_at")
    return render(request, "pieces/index.html", {"pieces": pieces})


# Upload a new document (file OR HTML paste)
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

            # --- File upload path ---
            if doc.uploaded_file:
                try:
                    (
                        html_content,
                        word_count,
                        char_count,
                        sentence_count,
                        line_count,
                        paragraph_count,
                        syllable_count,
                    ) = process_docx(doc.uploaded_file.path)

                    doc.formatted_text = html_content
                    doc.word_count = word_count
                    doc.char_count = char_count
                    doc.sentence_count = sentence_count
                    doc.line_count = line_count
                    doc.paragraph_count = paragraph_count
                    doc.syllable_count = syllable_count

                except Exception as e:
                    messages.error(request, f"Could not process file: {e}")
                    return render(request, "uploader.html", {"form": form})

            # --- HTML paste path ---
            elif doc.formatted_text:
                try:
                    (
                        html_content,
                        word_count,
                        char_count,
                        sentence_count,
                        line_count,
                        paragraph_count,
                        syllable_count,
                    ) = process_html(doc.formatted_text)

                    doc.formatted_text = html_content
                    doc.word_count = word_count
                    doc.char_count = char_count
                    doc.sentence_count = sentence_count
                    doc.line_count = line_count
                    doc.paragraph_count = paragraph_count
                    doc.syllable_count = syllable_count

                except Exception as e:
                    messages.error(request, f"Could not process HTML: {e}")
                    return render(request, "uploader.html", {"form": form})

            doc.save()
            return redirect("document_detail", slug=doc.slug)
    else:
        form = DocumentForm()

    return render(request, "uploader.html", {"form": form})


# Detail view with per-line analysis
def document_detail(request, slug):
    document = get_object_or_404(Document, slug=slug)

    line_stats = []
    scanned_text = None

    if document.uploaded_file:
        try:
            line_stats = process_docx_perline(document.uploaded_file.path)
        except Exception as e:
            line_stats = [{"text": f"Error: {e}", "words": 0, "syllables": 0}]
    elif document.formatted_text:
        try:
            line_stats = process_html_perline(document.formatted_text)
        except Exception as e:
            line_stats = [{"text": f"Error: {e}", "words": 0, "syllables": 0}]

    # Placeholder scansion (later we replace with real stress markers)
    if document.formatted_text:
        scanned_text = document.formatted_text.replace(
            "<p", "<p class='scanned'"  # simple marker
        )

    # Define available tools for the toolbar
    tools = [
        {"label": "Toggle Scansion", "js_function": "toggleScansion", "disabled": False},
        {"label": "Meter (soon)", "js_function": "toggleMeter", "disabled": True},
        {"label": "Heatmap (soon)", "js_function": "toggleHeatmap", "disabled": True},
    ]

    return render(request, "pieces/detail.html", {
        "document": document,
        "line_stats": line_stats,
        "scanned_text": scanned_text,
        "tools": tools,
    })