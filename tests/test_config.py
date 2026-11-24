"""Тесты валидации конфигурации (этап 1)."""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import (
    ConfigError,
    validate_depth,
    validate_output,
    validate_package,
    validate_source,
    validate_version,
)

def test_package_ok():
    """Проверка корректного пакета."""
    assert validate_package("  express ") == "express"

@pytest.mark.parametrize("bad", ["", "   ", "my package"])
def test_package_bad(bad):
    """Проверка некорректного пакета."""
    with pytest.raises(ConfigError):
        validate_package(bad)

def test_source_url_ok():
    """Проверка корректного URL."""
    assert validate_source("https://github.com/x/y", False).startswith("https://")

def test_source_url_bad():
    """Проверка некорректного URL."""
    with pytest.raises(ConfigError):
        validate_source("not-a-url", False)

def test_source_test_mode_missing_file():
    """Проверка отсутствующего файла в тестовом режиме."""
    with pytest.raises(ConfigError):
        validate_source("/no/such/file.txt", True)

def test_source_test_mode_empty_file(tmp_path):
    """Проверка пустого файла в тестовом режиме."""
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")
    with pytest.raises(ConfigError):
        validate_source(str(file), True)

def test_source_test_mode_ok(tmp_path):
    """Проверка корректного файла в тестовом режиме."""
    file = tmp_path / "repo.txt"
    file.write_text("A B", encoding="utf-8")
    assert validate_source(str(file), True) == str(file)

def test_version_bad():
    """Проверка пустой версии."""
    with pytest.raises(ConfigError):
        validate_version("")

def test_output_bad_dir(tmp_path):
    """Проверка, что вывод не может быть каталогом."""
    with pytest.raises(ConfigError):
        validate_output(str(tmp_path))

def test_output_bad_extension(tmp_path):
    """Проверка некорректного расширения."""
    with pytest.raises(ConfigError):
        validate_output(str(tmp_path / "graph.txt"))

def test_depth_bounds():
    """Проверка границ глубины."""
    assert validate_depth(0) == 0
    with pytest.raises(ConfigError):
        validate_depth(-1)
    with pytest.raises(ConfigError):
        validate_depth(10_000)