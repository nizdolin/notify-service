from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl, validator
from typing import Union


class APPSettings(BaseSettings):
    PROJECT_NAME: str = 'skill_notify'
    DEBUG: bool = True
    DATABASE_URI: PostgresDsn
    ROOT_PATH: str = ''

    INFO_LOG_FILE = 'app/logs/' + PROJECT_NAME + '_info.log'
    ERROR_LOG_FILE = 'app/logs/' + PROJECT_NAME + '_error.log'

    AUTH_SERVICE_URL: str

    OPENAPI_URL: Union[str, None]

    class Config:
        env_file = '.env'

    @validator('OPENAPI_URL', pre=True)
    def generate_docs_url(cls, v, values):
        if values.get('DEBUG'):
            return '/openapi.json'
        return None

    load_dotenv()


@lru_cache()
def get_app_settings() -> APPSettings:
    return APPSettings()
