from .pdf_parser import PDFParser
from .ocr import OCRProcessor
from .text_cleaner import TextCleaner
import os

async def ingest_document(file_bytes: bytes, filename: str) -> dict:
    pdf_parser = PDFParser()
    ocr = OCRProcessor()
    cleaner = TextCleaner()
    
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == '.pdf':
        res = pdf_parser.extract_from_bytes(file_bytes)
        if len(res['raw_text'].strip()) < 100:
            res = ocr.extract_from_pdf_images(file_bytes)
    elif ext in ['.jpg', '.jpeg', '.png']:
        res = ocr.extract_from_image(file_bytes)
    elif ext == '.txt':
        text = file_bytes.decode('utf-8', errors='replace')
        res = {
            "raw_text": text,
            "pages": [text],
            "page_count": 1,
            "extraction_method": "text"
        }
    else:
        raise ValueError("Unsupported file format")
        
    cleaned_text = cleaner.clean(res['raw_text'])
    res['text'] = cleaned_text
    res['token_estimate'] = pdf_parser.estimate_token_count(cleaned_text)
    res['file_size_kb'] = len(file_bytes) / 1024
    res['filename'] = filename
    res['language'] = cleaner.detect_language(cleaned_text)
    
    del res['raw_text']
    
    return res
