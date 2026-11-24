"""Тесты валидации конфигурации (этап 1)."""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import (
    ConfigError,
    validate_depth,
    validate_package,
    validate_source,
    validate_version,
)

def test_package_ok():
    assert validate_package("  express ") == "express"

@pytest.mark.parametrize("bad", ["", "   ", "my package"])
def test_package_bad(bad):
    with pytest.raises(ConfigError):
        validate_package(bad)

def test_source_url_ok():
    assert validate_source("https://github.com/x/y", False).startswith("https://")

def test_source_url_bad():
    with pytest.raises(ConfigError):
        validate_source("not-a-url", False)

def test_version_bad():
    with pytest.raises(ConfigError):
        validate_version("")

def test_depth_bounds():
    assert validate_depth(0) == 0
    with pytest.raises(ConfigError):
        validate_depth(-1)
    with pytest.raises(ConfigError):
        validate_depth(10_000)