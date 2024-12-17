import pytest

from OpenAIChatHelper.utils import (
    disable_all_loggers,
    enable_all_loggers,
    set_all_loggers_levels,
    set_default_logging_level,
)


def test_disable_all_loggers():
    assert disable_all_loggers() == True


def test_enable_all_loggers():
    assert enable_all_loggers() == True


def test_set_all_loggers_levels():
    assert set_all_loggers_levels("DEBUG") == True


def test_set_default_logging_level():
    assert set_default_logging_level("DEBUG") == True
