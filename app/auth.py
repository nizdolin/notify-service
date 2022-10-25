from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from app.core.config import get_app_settings

settings = get_app_settings()
api_key_header = APIKeyHeader(name='Authorization', auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.API_KEY:
        return api_key_header

    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Could not validate credentials')
