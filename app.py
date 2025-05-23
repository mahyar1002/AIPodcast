from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from utils.enums import EnvEnum
from config.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS
)
app.include_router(router)

if settings.ENV == EnvEnum.PRODUCTION.value:
    app.openapi_url = ""


@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME}: Service is up and running.."}
