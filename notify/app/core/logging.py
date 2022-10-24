import logging
import sys
from pathlib import Path
from loguru import logger
import json

from ..core.config import get_app_settings

config = get_app_settings()


# Custom Logger Using Loguru


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info,
        ).log(level, record.getMessage())


class CustomizeLogger:

    @classmethod
    def make_logger(cls):
        config_path = Path(__file__).with_name("logging.json")
        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')

        logger = cls.customize_logging(
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            format=logging_config.get('format')
        )
        return logger

    @classmethod
    def customize_logging(
            cls,
            level: str,
            rotation: str,
            retention: str,
            format: str
    ):
        logger.remove()
        logger.add(
            sys.stdout,
            colorize=True,
            diagnose=config.DEBUG,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
            catch=True,
        )
        logger.add(
            config.INFO_LOG_FILE,
            colorize=False,
            diagnose=config.DEBUG,
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level='INFO',
            format=format,
            filter=cls.info_only,
            catch=True,
        )
        logger.add(
            config.ERROR_LOG_FILE,
            colorize=False,
            diagnose=config.DEBUG,
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level='ERROR',
            format=format,
            catch=True,
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        for _log in [
            'uvicorn.access',
            'databases',
        ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config

    @staticmethod
    def info_only(record):
        return record["level"].name == "INFO"
