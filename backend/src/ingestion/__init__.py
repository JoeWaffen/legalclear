from .pdf_parser import PDFParser
from .ocr import OCRProcessor
from .text_cleaner import TextCleaner

_pdf = PDFParser()
_ocr = OCRProcessor()
_cleaner = TextCleaner()


async def ingest_document(file_bytes: bytes,
                          filename: str) -> dict:
    if len(file_bytes) > 15_000_000:
        return {
            "error": True,
            "error_code": "document_too_large",
            "message_en": (
                "This document is too large to process. "
                "Please upload sections under 15MB."),
            "message_es": (
                "Este documento es demasiado grande. "
                "Suba secciones de menos de 15MB.")
        }

    ext = (filename.rsplit(".", 1)[-1].lower()
           if "." in filename else "")

    if ext not in ["pdf", "jpg", "jpeg", "png",
                   "webp", "tiff", "bmp", "txt"]:
        if file_bytes[:4] == b"%PDF":
            ext = "pdf"
        elif file_bytes[:2] == b"\xff\xd8":
            ext = "jpg"
        elif file_bytes[:4] == b"\x89PNG":
            ext = "png"
        else:
            return {
                "error": True,
                "error_code": "unsupported_format",
                "message_en": (
                    "Unsupported file type. Please upload "
                    "a PDF, image, or text file."),
                "message_es": (
                    "Tipo de archivo no compatible.")
            }

    if ext == "pdf":
        result = _pdf.extract_from_bytes(file_bytes)
        if len(result["raw_text"].strip()) < 100:
            result = _ocr.extract_from_pdf_images(file_bytes)
            result["extraction_method"] = "ocr_fallback"
    elif ext in ["jpg", "jpeg", "png",
                 "webp", "tiff", "bmp"]:
        result = _ocr.extract_from_image(file_bytes)
    else:
        raw_text = file_bytes.decode("utf-8", errors="replace")
        result = {
            "raw_text": raw_text,
            "pages": [raw_text],
            "page_count": 1,
            "file_size_kb": round(len(file_bytes) / 1024, 2),
            "extraction_method": "text"
        }

    cleaned = _cleaner.clean(result["raw_text"])
    language = _cleaner.detect_language(cleaned)
    truncated = _cleaner.truncate_for_llm(cleaned)
    token_estimate = _pdf.estimate_token_count(cleaned)

    return {
        "text": truncated,
        "raw_text": cleaned,
        "pages": result.get("pages", []),
        "page_count": result.get("page_count", 1),
        "token_estimate": token_estimate,
        "file_size_kb": result.get("file_size_kb", 0.0),
        "extraction_method": result.get(
            "extraction_method", "unknown"),
        "filename": filename,
        "language": language,
        "truncated": len(truncated) < len(cleaned),
        "error": False
    }
