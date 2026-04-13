import pytesseract
from PIL import Image, ImageEnhance
import io
import fitz

class OCRProcessor:
    def __init__(self):
        pass
        
    def extract_from_image(self, file_bytes: bytes, lang: str = 'eng') -> dict:
        tesseract_lang = 'spa' if lang == 'spa' else 'eng'
        image = Image.open(io.BytesIO(file_bytes)).convert('L')
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        text = pytesseract.image_to_string(image, lang=tesseract_lang)
        
        return {
            "raw_text": text,
            "pages": [text],
            "page_count": 1,
            "confidence": 0.8,
            "extraction_method": "ocr"
        }

    def extract_from_pdf_images(self, file_bytes: bytes, lang: str = 'eng') -> dict:
        tesseract_lang = 'spa' if lang == 'spa' else 'eng'
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        
        raw_text = ""
        pages = []
        
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes()))
            img = img.convert('L')
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            
            text = pytesseract.image_to_string(img, lang=tesseract_lang)
            raw_text += text + "\n"
            pages.append(text)
            
        return {
            "raw_text": raw_text,
            "pages": pages,
            "page_count": len(pages),
            "confidence": 0.8,
            "extraction_method": "ocr"
        }
