import logging
from typing import Any

import sys
from os import environ as env

from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

load_dotenv()
LOG_LEVEL = env.get("LOG_LEVEL", "INFO")

HOST_PORT = env.get("HOST_PORT", "8080")


def setup_logging() -> None:
    """Initiate logger."""
    logger = logging.getLogger()
    logger.setLevel(str(LOG_LEVEL))

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(StackdriverJsonFormatter())
    log_handler.addFilter(PingFilter())
    log_handler.addFilter(ReadyFilter())
    log_handler.addFilter(BlackboxExporterFilter())
    log_handler.addFilter(RdfLibFailedXsdLiteralConversionFilter())
    logger.addHandler(log_handler)


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    """json log formatter."""

    def __init__(
        self: Any,
        fmt: str = "%(levelname) %(message)",
        style: str = "%",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init json-logger."""
        jsonlogger.JsonFormatter.__init__(self, *args, **kwargs, fmt=fmt)

    def process_log_record(self: Any, log_record: Any) -> Any:
        """Process log record to a json-format compatible with Stackdriver."""
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        log_record["serviceContext"] = {"service": "fdk-atlas-dcat-service"}
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)


class PingFilter(logging.Filter):
    """Custom Ping Filter class."""

    def filter(self: Any, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /ping" not in record.getMessage()


class ReadyFilter(logging.Filter):
    """Custom Ready Filter class."""

    def filter(self: Any, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /ready" not in record.getMessage()


class BlackboxExporterFilter(logging.Filter):
    """Custom Blackbox Exporter Filter class."""

    def filter(self: Any, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "Blackbox Exporter" not in record.getMessage()


class RdfLibFailedXsdLiteralConversionFilter(logging.Filter):
    """Custom Blackbox Exporter Filter class."""

    def filter(self: Any, record: logging.LogRecord) -> bool:
        """Filter function."""
        return (
            "Failed to convert Literal lexical form to value" not in record.getMessage()
        )
