"""Загрузка package.json из удалённого npm-репозитория.

Запрещено использовать менеджеры пакетов и сторонние библиотеки
для получения информации о зависимостях.
"""

import json
import urllib.request
from urllib.error import HTTPError, URLError

REQUEST_TIMEOUT = 10


class FetchError(RuntimeError):
    """Ошибка получения данных о пакете."""


def fetch_package_json(url: str) -> dict:
    """Скачивает и парсит package.json по URL."""
    try:
        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as response:
            raw = response.read()
    except HTTPError as error:
        raise FetchError(f"HTTP-ошибка {error.code} при загрузке {url}") from error
    except URLError as error:
        raise FetchError(f"Сетевая ошибка при загрузке {url}: {error.reason}") from error
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FetchError(f"Некорректный package.json в {url}: {error}") from error
    if not isinstance(data, dict):
        raise FetchError(f"Ожидался JSON-объект в {url}.")
    return data