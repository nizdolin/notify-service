from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import notification
from app.core.config import get_app_settings
from app.core.logging import CustomizeLogger
from app.db.db import init_db
from app.db.models import *

settings = get_app_settings()


def get_app() -> FastAPI:
    server = FastAPI(
        title=settings.PROJECT_NAME,
        root_path=settings.ROOT_PATH,
        openapi_url=settings.OPENAPI_URL,
    )

    notification_api = FastAPI(title=f"{settings.PROJECT_NAME} NOTIFICATION")
    notification_api.include_router(notification.router, tags=["notification"])
    server.mount("/api/notification", notification_api)

    server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    server.logger = CustomizeLogger.make_logger()

    @server.on_event("startup")
    def startup():
        init_db()

    return server


app = get_app()
