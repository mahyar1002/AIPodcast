import os
import uvicorn
from utils.enums import EnvEnum
from config.settings import settings

if __name__ == "__main__":
    if os.getenv("ENV") == EnvEnum.DEV.value:
        uvicorn.run('app:app', host=settings.API_HOST,
                    port=settings.API_PORT, reload=True)
    else:
        uvicorn.run('app:app', host=settings.API_HOST,
                    port=settings.API_PORT, reload=False, workers=4)
