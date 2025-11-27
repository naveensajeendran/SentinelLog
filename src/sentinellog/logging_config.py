import logging
from logging.config import dictConfig
from pathlib import Path
from .config import config

LOG_FILE = Path(config.LOG_DIR) / "sentinel.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def setup_logging():
    dictConfig({
        "version": 1,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
            "json": {
                "format": '{"time": "%(asctime)s", "level": "%(levelname)s", '
                          '"logger": "%(name)s", "message": "%(message)s"}'
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": "INFO"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(LOG_FILE),
                "maxBytes": 2*1024*1024,
                "backupCount": 5,
                "formatter": "standard",
                "level": "INFO"
            }
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO"
        }
    })

# Initialize logging when imported
setup_logging()