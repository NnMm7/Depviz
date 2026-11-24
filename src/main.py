"""CLI-прототип инструмента визуализации графа зависимостей (этап 1)."""

import sys
from config import ConfigError, build_config, parse_args, print_config

def main(argv: list[str] | None = None) -> int:
    """Точка входа приложения."""
    args = parse_args(argv)
    try:
        config = build_config(args)
    except ConfigError as error:
        print(f"Ошибка конфигурации: {error}", file=sys.stderr)
        return 2
    print_config(config)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())