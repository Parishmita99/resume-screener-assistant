
from io import BytesIO
from pypdf import PdfReader
from docx import Document


def extract_resume_text(uploaded_file):
    """
    Extract text from TXT, PDF or DOCX uploaded files.
    Returns extracted text as a string.
    """

    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if file_name.endswith(".txt"):
        return file_bytes.decode("utf-8-sig")

    elif file_name.endswith(".pdf"):
        pdf = PdfReader(BytesIO(file_bytes))

        pages = []

        for page in pdf.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    elif file_name.endswith(".docx"):
        document = Document(BytesIO(file_bytes))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    else:
        raise ValueError(
            "Unsupported file format. Upload TXT, PDF or DOCX."
        )
