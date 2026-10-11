
from pathlib import Path
import pymupdf


def read_pdf_file(file_path: str) -> str:
    """Extract text from a PDF study document."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    extracted_pages = []

    with pymupdf.open(path) as document:
        for page in document:
            page_text = page.get_text()
            if page_text.strip():
                extracted_pages.append(page_text)

    return "\n".join(extracted_pages).strip()


if __name__ == "__main__":
    pdf_path = input("Enter the path to your PDF: ").strip().strip('"')

    text = read_pdf_file(pdf_path)

    print("\nPDF loaded successfully!")
    print(f"Characters extracted: {len(text)}")
    print("\nPreview:\n")
    print(text[:500])
