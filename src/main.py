"""CLI-инструмент визуализации графа зависимостей (этап 2)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config, ConfigError, build_config, parse_args, print_config
from fetcher import FetchError, fetch_package_json
from npm_parser import extract_direct_dependencies


def run_stage_two(config: Config) -> int:
    """Получает и выводит прямые зависимости пакета."""
    if config.test_mode:
        print(
            "Этап 2 не поддерживает тестовый режим, "
            "используйте этап 3 для работы с файлом-описанием.",
            file=sys.stderr,
        )
        return 3
    print_config(config)
    try:
        package_json = fetch_package_json(config.source)
    except FetchError as error:
        print(f"Ошибка получения данных: {error}", file=sys.stderr)
        return 4
    dependencies = extract_direct_dependencies(package_json)
    print("direct_dependencies:")
    for name in dependencies:
        print(f"- {name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Точка входа приложения."""
    args = parse_args(argv)
    try:
        config = build_config(args)
    except ConfigError as error:
        print(f"Ошибка конфигурации: {error}", file=sys.stderr)
        return 2
    return run_stage_two(config)


if __name__ == "__main__":
    raise SystemExit(main())