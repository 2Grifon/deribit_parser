from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.routes.index_price import index_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Deribit Parser",
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

main_router = APIRouter(prefix="/api", tags=["API"])

main_router.include_router(index_router)

app.include_router(main_router)
