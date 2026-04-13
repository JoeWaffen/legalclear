import uvicorn
from src.api.routes import app
from src.core.config import settings

if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
        reload=settings.is_development
    )
