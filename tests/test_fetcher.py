"""Тесты загрузчика package.json."""

import io
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fetcher import FetchError, fetch_package_json


class _FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def test_fetch_ok(monkeypatch):
    """Проверка успешной загрузки."""
    payload = json.dumps({"name": "x", "dependencies": {"a": "1"}}).encode()

    def fake_urlopen(url, timeout):
        assert timeout > 0
        return _FakeResponse(payload)

    monkeypatch.setattr("fetcher.urllib.request.urlopen", fake_urlopen)
    data = fetch_package_json("https://example.com/package.json")
    assert data["name"] == "x"


def test_fetch_invalid_json(monkeypatch):
    """Проверка невалидного JSON."""
    def fake_urlopen(url, timeout):
        return _FakeResponse(b"not a json")

    monkeypatch.setattr("fetcher.urllib.request.urlopen", fake_urlopen)
    with pytest.raises(FetchError):
        fetch_package_json("https://example.com/package.json")