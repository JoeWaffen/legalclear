import fitz  # PyMuPDF

class PDFParser:
    def __init__(self):
        pass
        
    def extract_text(self, file_path: str) -> dict:
        try:
            doc = fitz.open(file_path)
            raw_text = ""
            pages = []
            
            for page in doc:
                text = page.get_text()
                raw_text += text + "\n"
                pages.append(text)
                
            return {
                "raw_text": raw_text,
                "pages": pages,
                "page_count": len(pages),
                "file_size_kb": 0, # Cannot know easily from Document level without os.path
                "extraction_method": "pdf"
            }
        except Exception as e:
            raise Exception(f"Failed to extract PDF: {e}")

    def extract_from_bytes(self, file_bytes: bytes) -> dict:
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            raw_text = ""
            pages = []
            
            for page in doc:
                text = page.get_text()
                raw_text += text + "\n"
                pages.append(text)
                
            return {
                "raw_text": raw_text,
                "pages": pages,
                "page_count": len(pages),
                "file_size_kb": len(file_bytes) / 1024,
                "extraction_method": "pdf"
            }
        except Exception as e:
             raise Exception(f"Failed to extract PDF from bytes: {e}")

    def estimate_token_count(self, text: str) -> int:
        return int(len(text.split()) * 1.3)
