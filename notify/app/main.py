from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from app.api import ping
from app.api.v1 import router
from app.core.config import get_app_settings
from app.core.logging import CustomizeLogger
from app.db.db import init_db
from app.db.models import *

app_settings = get_app_settings()


def get_app() -> FastAPI:
    server = FastAPI(
        title=app_settings.PROJECT_NAME,
        root_path=app_settings.ROOT_PATH,
        openapi_url=app_settings.OPENAPI_URL,
    )

    server.include_router(ping.router, tags=["health"])

    # server.include_router(client.router, tags=["client"])

    service_api = FastAPI(title=f"{app_settings.PROJECT_NAME} SERVICE")
    service_api.include_router(router.router, tags=["notification"])
    server.mount("/api/notification", service_api)

    # admin_api = FastAPI(title=f"{app_settings.PROJECT_NAME} ADMIN")
    # admin_api.include_router(admin.router, tags=["admin"])
    # server.mount("/admin", admin_api)

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
