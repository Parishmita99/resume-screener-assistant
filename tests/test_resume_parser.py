
from io import BytesIO
from docx import Document
from pypdf import PdfWriter
from resume_parser import extract_resume_text


class FakeUploadedFile:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def getvalue(self):
        return self.content


def test_txt_extraction():
    file = FakeUploadedFile(
        "resume.txt",
        b"Python Developer with SQL experience"
    )

    result = extract_resume_text(file)

    assert "Python Developer" in result


def test_docx_extraction():
    document = Document()
    document.add_paragraph("Candidate: Rahul Sharma")
    document.add_paragraph("Skills: Python and SQL")

    buffer = BytesIO()
    document.save(buffer)

    file = FakeUploadedFile(
        "resume.docx",
        buffer.getvalue()
    )

    result = extract_resume_text(file)

    assert "Rahul Sharma" in result
    assert "Python and SQL" in result


def test_pdf_extraction():
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    buffer = BytesIO()
    writer.write(buffer)

    file = FakeUploadedFile(
        "resume.pdf",
        buffer.getvalue()
    )

    result = extract_resume_text(file)

    assert isinstance(result, str)
