from pathlib import Path
import pymupdf
from docx import Document
import pandas as pd


def extract_pdf_pages(file_path: str) -> list[dict]:
    """
    Extract PDF text while preserving page numbers.
    """

    pages = []

    pdf = pymupdf.open(file_path)

    try:
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text().strip()

            if page_text:
                pages.append({
                    "page": page_number,
                    "text": page_text
                })

    finally:
        pdf.close()

    return pages


def extract_pdf(file_path: str) -> str:
    """
    Extract all PDF text as one string.
    """

    pages = extract_pdf_pages(file_path)

    return "\n\n".join(
        f"[Page {page['page']}]\n{page['text']}"
        for page in pages
    )


def extract_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text.strip())

    return "\n\n".join(paragraphs)


def extract_txt(file_path: str) -> str:
    """
    Extract text from a TXT file.
    """

    return Path(file_path).read_text(
        encoding="utf-8"
    )


def extract_csv(file_path: str) -> str:
    """
    Convert CSV rows into searchable text.
    """

    dataframe = pd.read_csv(file_path)

    return dataframe.to_string(index=False)


def extract_text(file_path: str) -> str:
    """
    Automatically select the correct parser
    based on file extension.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    elif extension == ".docx":
        return extract_docx(file_path)

    elif extension == ".txt":
        return extract_txt(file_path)

    elif extension == ".csv":
        return extract_csv(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )