from pathlib import Path
from pypdf import PdfReader

def load_pdf_folder(folder_path):
    """Read every PDF and return a list of page-level documents."""
    documents = []

    for pdf_path in Path(folder_path).glob("*.pdf"):
        reader = PdfReader(str(pdf_path))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                documents.append({
                    "text": text,
                    "source": pdf_path.name,
                    "page": page_number
                })

    return documents
