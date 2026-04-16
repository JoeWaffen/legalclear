import fitz
import os


class PDFParser:

    def extract_text(self, file_path: str) -> dict:
        doc = fitz.open(file_path)
        pages = [page.get_text() for page in doc]
        raw_text = "\n".join(pages)
        file_size_kb = os.path.getsize(file_path) / 1024
        return {
            "raw_text": raw_text,
            "pages": pages,
            "page_count": len(pages),
            "file_size_kb": round(file_size_kb, 2),
            "extraction_method": "pdf"
        }

    def extract_from_bytes(self, file_bytes: bytes) -> dict:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages = [page.get_text() for page in doc]
        raw_text = "\n".join(pages)
        return {
            "raw_text": raw_text,
            "pages": pages,
            "page_count": len(pages),
            "file_size_kb": round(len(file_bytes) / 1024, 2),
            "extraction_method": "pdf"
        }

    def estimate_token_count(self, text: str) -> int:
        return int(len(text.split()) * 1.3)
