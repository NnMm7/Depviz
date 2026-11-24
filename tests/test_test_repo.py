"""Тесты загрузчика тестового репозитория (этап 3)."""
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from test_repo import load_graph_from_file, TestRepoError

def test_load_simple(tmp_path):
    file = tmp_path / "repo.txt"
    file.write_text("A B C\nB D\n", encoding="utf-8")
    graph = load_graph_from_file(str(file))
    assert graph.children("A") == ["B", "C"]

def test_load_rejects_lowercase(tmp_path):
    file = tmp_path / "repo.txt"
    file.write_text("a B\n", encoding="utf-8")
    with pytest.raises(TestRepoError):
        load_graph_from_file(str(file))