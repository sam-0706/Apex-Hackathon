import os
import fitz  # PyMuPDF

def extract_text_from_pdf(path: str) -> str:
    """
    Extracts text from a text-based PDF (no OCR).

    Args:
        path (str): Path to the PDF file.

    Returns:
        str: Extracted text content.

    Raises:
        RuntimeError: If the file is not a PDF or no text is found.
    """
    if not path.lower().endswith(".pdf"):
        raise RuntimeError(f"Unsupported file type (only .pdf allowed): {path}")

    if not os.path.exists(path):
        raise RuntimeError(f"File does not exist: {path}")

    try:
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                page_text = page.get_text("text").strip()
                text += page_text + "\n"

        if not text.strip():
            raise RuntimeError(f"No text found in PDF (possibly image-based): {path}")

        return text

    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}") from e


# Optional: test run block
if __name__ == "__main__":
    test_pdf = "Shivaji_s_Resume.pdf"
    try:
        extracted = extract_text_from_pdf(test_pdf)
        print("Extracted Text:\n")
        print(extracted)
    except RuntimeError as e:
        print(f"Error: {e}")
