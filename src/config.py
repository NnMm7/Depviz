"""Конфигурация приложения: разбор и валидация параметров."""

import argparse
import os
from dataclasses import dataclass
from urllib.parse import urlparse

MIN_DEPTH = 0
MAX_DEPTH_LIMIT = 100
DEFAULT_DEPTH = 3
DEFAULT_VERSION = "latest"
DEFAULT_OUTPUT = "graph.png"
ALLOWED_EXTENSIONS = (".png", ".svg", ".pdf")


class ConfigError(ValueError):
    """Ошибка конфигурации, связанная с некорректным параметром."""


@dataclass(frozen=True)
class Config:
    """Настраиваемые пользователем параметры."""

    package: str
    source: str
    test_mode: bool
    version: str
    output_file: str
    max_depth: int


def _positive_int(value: str) -> int:
    """Преобразует строку в целое неотрицательное число."""
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"Ожидается целое число, получено: {value!r}"
        ) from error
    if number < MIN_DEPTH:
        raise argparse.ArgumentTypeError(
            f"Значение не может быть меньше {MIN_DEPTH}."
        )
    return number


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        prog="depviz",
        description="Визуализация графа зависимостей npm-пакета.",
    )
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета")
    parser.add_argument(
        "--source",
        required=True,
        help="URL репозитория или путь к файлу тестового репозитория",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Режим работы с тестовым репозиторием",
    )
    parser.add_argument("--pkg-version", default=DEFAULT_VERSION, help="Версия пакета")
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Имя файла с изображением графа",
    )
    parser.add_argument(
        "--max-depth",
        type=_positive_int,
        default=DEFAULT_DEPTH,
        help="Максимальная глубина анализа зависимостей",
    )
    return parser.parse_args(argv)


def validate_package(package: str) -> str:
    """Проверяет имя пакета."""
    value = package.strip()
    if not value:
        raise ConfigError("Имя пакета не может быть пустым.")
    if any(ch.isspace() for ch in value):
        raise ConfigError("Имя пакета не должно содержать пробелов.")
    return value


def validate_source(source: str, test_mode: bool) -> str:
    """Проверяет URL репозитория или путь к тестовому файлу."""
    value = source.strip()
    if not value:
        raise ConfigError("Источник не может быть пустым.")
    if test_mode:
        if not os.path.isfile(value):
            raise ConfigError(f"Файл тестового репозитория не найден: {value}")
        if os.path.getsize(value) == 0:
            raise ConfigError(f"Файл тестового репозитория пуст: {value}")
        return value
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ConfigError("Ожидается корректный URL (http/https) либо --test-mode.")
    return value


def validate_version(version: str) -> str:
    """Проверяет версию пакета."""
    value = version.strip()
    if not value:
        raise ConfigError("Версия пакета не может быть пустой.")
    return value


def validate_output(output: str) -> str:
    """Проверяет имя выходного файла."""
    value = output.strip()
    if not value:
        raise ConfigError("Имя файла изображения не может быть пустым.")
    if os.path.isdir(value):
        raise ConfigError(f"Ожидается файл, а не каталог: {value}")
    directory = os.path.dirname(os.path.abspath(value)) or "."
    if not os.path.isdir(directory):
        raise ConfigError(f"Каталог для вывода не существует: {directory}")
    if not value.lower().endswith(ALLOWED_EXTENSIONS):
        raise ConfigError(
            f"Расширение файла должно быть одним из: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return value


def validate_depth(depth: int) -> int:
    """Проверяет максимальную глубину анализа."""
    if depth < MIN_DEPTH:
        raise ConfigError(f"Глубина не может быть меньше {MIN_DEPTH}.")
    if depth > MAX_DEPTH_LIMIT:
        raise ConfigError(f"Глубина не может превышать {MAX_DEPTH_LIMIT}.")
    return depth


def build_config(args: argparse.Namespace) -> Config:
    """Собирает и валидирует конфигурацию."""
    return Config(
        package=validate_package(args.package),
        source=validate_source(args.source, args.test_mode),
        test_mode=args.test_mode,
        version=validate_version(args.pkg_version),
        output_file=validate_output(args.output),
        max_depth=validate_depth(args.max_depth),
    )


def print_config(config: Config) -> None:
    """Выводит параметры в формате ключ-значение."""
    print(f"package={config.package}")
    print(f"source={config.source}")
    print(f"test_mode={config.test_mode}")
    print(f"pkg_version={config.version}")
    print(f"output_file={config.output_file}")
    print(f"max_depth={config.max_depth}")