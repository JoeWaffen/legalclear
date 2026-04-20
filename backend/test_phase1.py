import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.ingestion import ingest_document


async def run():
    with open("test_lease.pdf", "rb") as f:
        data = f.read()

    result = await ingest_document(data, "test_lease.pdf")
    assert not result["error"], f"Error: {result}"
    assert result["extraction_method"] in [
        "pdf", "ocr_fallback"]
    assert result["language"] == "en"
    assert result["token_estimate"] > 0
    assert len(result["text"]) > 50
    print(f"method: {result['extraction_method']}")
    print(f"language: {result['language']}")
    print(f"tokens: {result['token_estimate']}")
    print(f"preview: {result['text'][:150]}")

    big = await ingest_document(b"x" * 20_000_000, "big.pdf")
    assert big["error"]
    assert big["error_code"] == "document_too_large"
    print("Size gate OK")

    bad = await ingest_document(b"garbage data", "file.xyz")
    assert bad["error"]
    print("Format gate OK")

    print("\nALL PHASE 1 ASSERTIONS PASSED")


asyncio.run(run())
