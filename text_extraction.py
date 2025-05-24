# text_extractor.py
"""
Simple document-to-text extractor.

Example
-------
from text_extractor import extract_text
raw = extract_text("/absolute/or/relative/path/resume.pdf")
"""

from __future__ import annotations
import os
import subprocess

import fitz                      # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
from PIL import Image            # noqa: F401  (needed by pytesseract)
import docx2txt

# temporary location for LibreOffice conversions
_CONVERT_DIR = os.path.join(os.path.dirname(__file__), "_converted")
os.makedirs(_CONVERT_DIR, exist_ok=True)

_SUPPORTED = (".pdf", ".docx", ".doc", ".txt")

# --------------------------------------------------------------------------- #
# Internal helpers
# --------------------------------------------------------------------------- #
def _convert_to_pdf(src: str) -> str | None:
    """DOC / DOCX ➜ PDF via LibreOffice. Returns new path or None on failure."""
    pdf_name = os.path.splitext(os.path.basename(src))[0] + ".pdf"
    pdf_path = os.path.join(_CONVERT_DIR, pdf_name)
    try:
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf",
             "--outdir", _CONVERT_DIR, os.path.abspath(src)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return pdf_path if os.path.exists(pdf_path) else None
    except Exception:
        return None


def _is_text_pdf(path: str) -> bool:
    try:
        with fitz.open(path) as doc:
            return any(page.get_text().strip() for page in doc)
    except Exception:
        return False


def _pdf_text(path: str) -> str:
    if _is_text_pdf(path):
        with fitz.open(path) as doc:
            return "".join(page.get_text("text") for page in doc)
    images = convert_from_path(path, dpi=300)
    text = []
    for img in images:
        text.append(pytesseract.image_to_string(img, config="--psm 1"))
    return "".join(text)


def _docx_text(path: str) -> str:
    """
    Extract text from a .docx file by:
    - Converting it to PDF via LibreOffice
    - Then extracting text (PDF text or OCR)
    """
    pdf_path = _convert_to_pdf(path)
    if pdf_path:
        return _pdf_text(pdf_path)
    raise RuntimeError(f"Failed to extract text from .docx: {path}")



def _doc_text(path: str) -> str:
    """
    Extract text from a .doc file by:
    - Converting it to PDF via LibreOffice
    - Then extracting text (PDF text or OCR)
    """
    pdf_path = _convert_to_pdf(path)
    if pdf_path:
        return _pdf_text(pdf_path)
    raise RuntimeError(f"Failed to extract text from .doc: {path}")


def _txt_text(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def extract_text(path: str) -> str:
    """
    Extract raw text from a single file.

    Raises
    ------
    RuntimeError
        If the file type is unsupported or text cannot be extracted.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext not in _SUPPORTED:
        raise RuntimeError(f"Unsupported file type: {path}")

    try:
        if ext == ".pdf":
            text = _pdf_text(path)
        elif ext == ".docx":
            text = _docx_text(path)
        elif ext == ".doc":
            text = _doc_text(path)
        else:  # ".txt"
            text = _txt_text(path)
    except Exception as exc:
        raise RuntimeError(f"Extraction failed for {path}: {exc}") from exc

    if not text.strip():
        # fallback: convert to PDF and OCR
        pdf = _convert_to_pdf(path)
        if pdf:
            text = _pdf_text(pdf)

    if not text.strip():
        raise RuntimeError(f"No text could be extracted from {path}")

    return text


def main():
    # Replace this with the path to your file
    file_path = r"C:\Users\jeswa\projects\ocr-pipeline\Prod-OCR\data\data.doc"

    try:
        text = extract_text(file_path)
        print("Extracted Text:\n")
        print(text)
    except RuntimeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
