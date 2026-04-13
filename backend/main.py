import uvicorn
from src.api.routes import app
from src.core.config import settings

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=port,
        reload=settings.is_development
    )
