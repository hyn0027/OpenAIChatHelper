import logging
from typing import Union

LOG_COLORS = {
    "DEBUG": "\033[96m",  # Cyan
    "INFO": "\033[92m",  # Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "CRITICAL": "\033[1;91m",  # Bold Red
    "RESET": "\033[0m",  # Reset color
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, LOG_COLORS["RESET"])
        record.levelname = f"{log_color}[{record.levelname}]{LOG_COLORS['RESET']}"
        return super().format(record)


def get_logger(name, level: Union[int, str] = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = ColoredFormatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
