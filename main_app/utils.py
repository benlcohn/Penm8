from docx import Document
from bs4 import BeautifulSoup
import re

def process_docx(file_path: str) -> tuple[str, int, int, int, int, int]:
    """
    Read DOCX with python-docx, convert to HTML preserving
    paragraph alignment and inline styles (bold, italic, underline).
    Returns:
      (html_content, word_count, char_count, sentence_count, line_count, paragraph_count)
    """
    doc = Document(file_path)

    html_parts = []
    align_map = {
        0: "left",
        1: "center",
        2: "right",
        3: "justify",
    }

    for para in doc.paragraphs:
        if not para.text.strip():
            continue

        # Paragraph alignment
        align = align_map.get(para.paragraph_format.alignment, "left")
        para_html = f'<p style="text-align:{align};">'

        # Inline runs
        for run in para.runs:
            text = run.text.replace("\n", "<br>")  # preserve manual line breaks
            if not text:
                continue

            if run.bold:
                text = f"<b>{text}</b>"
            if run.italic:
                text = f"<i>{text}</i>"
            if run.underline:
                text = f"<u>{text}</u>"

            para_html += text

        para_html += "</p>"
        html_parts.append(para_html)

    # Final HTML
    html_content = "".join(html_parts)

    # Plain text for analysis
    soup = BeautifulSoup(html_content, "html.parser")
    plain_text = soup.get_text(separator="\n")  # keep line breaks for counting

    # Word & char counts
    words = plain_text.split()
    word_count = len(words)
    char_count = len(plain_text)

    # Sentence count
    sentences = re.split(r"[.!?]+(?:\s|$)", plain_text.strip())
    sentence_count = len([s for s in sentences if s.strip()])

    # Line count (based on newlines in plain text)
    line_count = len([line for line in plain_text.splitlines() if line.strip()])

    # Paragraph count (based on <p> tags we generated)
    paragraph_count = len(soup.find_all("p"))

    return (
        html_content,
        word_count,
        char_count,
        sentence_count,
        line_count,
        paragraph_count,
    )
