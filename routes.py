from fastapi import APIRouter
from api.routes import router as podcast_router
from config.settings import settings

router = APIRouter()
router.include_router(podcast_router, prefix=settings.API_STR)
