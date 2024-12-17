import logging
from typing import Union

_loggers = {}
_default_logging_level = logging.INFO

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


def get_logger(
    name: str, level: Union[int, str] = _default_logging_level
) -> logging.Logger:
    """Create a logger with the specified name and level.

    Args:
        name (str): _description_
        level (Union[int, str], optional): The verbose level . Defaults to logging.INFO.

    Returns:
        logging.Logger: The logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = ColoredFormatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    global _loggers
    _loggers[name] = logger
    return logger


def disable_logger(logger: Union[str, logging.Logger]) -> bool:
    """Disable a logger.

    Args:
        logger (Union[str, logging.Logger]): The logger to disable.

    Returns:
        bool: True if the logger was disabled, False otherwise.
    """
    if isinstance(logger, str):
        logger = _loggers.get(logger)
    if logger:
        logger.disabled = True
        return True
    return False


def disable_all_loggers():
    """disable_all_loggers."""
    for logger in _loggers.values():
        disable_logger(logger)


def enable_logger(logger: Union[str, logging.Logger]) -> bool:
    """Enable a logger.

    Args:
        logger (Union[str, logging.Logger]): The logger to enable.

    Returns:
        bool: True if the logger was enabled, False otherwise.
    """
    if isinstance(logger, str):
        logger = _loggers.get(logger)
    if logger:
        logger.disabled = False
        return True
    return False


def enable_all_loggers():
    """Enable all loggers."""
    for logger in _loggers.values():
        enable_logger(logger)


def set_logging_level(logger: Union[str, logging.Logger], level: Union[int, str]):
    """Set the logging level for a logger.

    Args:
        logger (Union[str, logging.Logger]): The logger to set the level for.
        level (Union[int, str]): The verbose level.
    """
    if isinstance(logger, str):
        logger = _loggers.get(logger)
    if logger:
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)


def set_all_logging_levels(level: Union[int, str]):
    """Set the logging level for all loggers.

    Args:
        level (Union[int, str]): The verbose level.
    """
    for logger in _loggers.values():
        set_logging_level(logger, level)


def set_default_logging_level(level: Union[int, str]):
    """Set the default logging level.

    Args:
        level (Union[int, str]): The verbose level.
    """
    global _default_logging_level
    _default_logging_level = level
    set_all_logging_levels(level)
