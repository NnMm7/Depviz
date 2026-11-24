"""Тесты разбора прямых зависимостей."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from npm_parser import extract_direct_dependencies, extract_package_name


def test_extract_dependencies_merges_sections():
    """Проверка объединения зависимостей из разных секций."""
    data = {
        "dependencies": {"a": "1", "b": "2"},
        "devDependencies": {"c": "3"},
        "peerDependencies": {"d": "4"},
        "optionalDependencies": {"a": "1"},
    }
    assert extract_direct_dependencies(data) == ["a", "b", "c", "d"]


def test_extract_package_name_ok():
    """Проверка извлечения имени пакета."""
    assert extract_package_name({"name": "  express  "}) == "express"


@pytest.mark.parametrize("bad", [{}, {"name": ""}, {"name": 42}])
def test_extract_package_name_bad(bad):
    """Проверка ошибок при извлечении имени."""
    with pytest.raises(ValueError):
        extract_package_name(bad)