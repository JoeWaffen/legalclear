import sys
sys.path.insert(0, '/home/joe/.gemini/antigravity/scratch/legalclear/backend')
import asyncio
from src.api.routes import upload_document
from fastapi.datastructures import UploadFile
import io

async def test():
    f = UploadFile(filename="doc.txt", file=io.BytesIO(b"This is a legitimate legal document. This is a legitimate legal document. This is a legitimate legal document. This is a legitimate legal document."))
    try:
        res = await upload_document(f, "123", "en")
        print(res)
    except Exception:
        import traceback
        traceback.print_exc()

asyncio.run(test())
