"""CLI-приложение для визуализации графа зависимостей."""
import argparse
import re
import sys

DEFAULT_OUTPUT = "graph.png"
DEFAULT_DEPTH = 3
MIN_DEPTH = 1
MAX_DEPTH = 10
VERSION_REGEX = r"^\d+\.\d+\.\d+$"

def validate_args(args: argparse.Namespace) -> None:
    """Валидация входных параметров.
    
    :param args: объект с аргументами командной строки.
    :raises SystemExit: если параметры некорректны.
    """
    if not args.package.strip():
        raise ValueError("Имя пакета не может быть пустым.")
    
    if not args.repo.strip():
        raise ValueError("URL репозитория или путь не может быть пустым.")

    if not re.match(VERSION_REGEX, args.version):
        raise ValueError(
            "Версия пакета должна соответствовать формату X.Y.Z (например, 1.0.0)."
        )

    if not (MIN_DEPTH <= args.max_depth <= MAX_DEPTH):
        raise ValueError(
            f"Глубина анализа должна быть от {MIN_DEPTH} до {MAX_DEPTH}."
        )

    if not args.output.endswith(('.png', '.svg', '.pdf', '.dot')):
        raise ValueError(
            "Имя выходного файла должно иметь расширение .png, .svg, .pdf или .dot."
        )

def print_config(args: argparse.Namespace) -> None:
    """Вывод всех настраиваемых параметров в формате ключ-значение."""
    print("--- Настраиваемые параметры ---")
    print(f"Имя анализируемого пакета: {args.package}")
    print(f"URL репозитория / путь: {args.repo}")
    print(f"Режим работы с тестовым репозиторием: {args.test_mode}")
    print(f"Версия пакета: {args.version}")
    print(f"Имя сгенерированного файла: {args.output}")
    print(f"Максимальная глубина анализа: {args.max_depth}")
    print("-------------------------------")

def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (Этап 1)."
    )
    
    parser.add_argument(
        "-p", "--package", type=str, required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "-r", "--repo", type=str, required=True,
        help="URL-адрес репозитория или путь к файлу тестового репозитория"
    )
    parser.add_argument(
        "-t", "--test-mode", action="store_true",
        help="Режим работы с тестовым репозиторием (флаг)"
    )
    parser.add_argument(
        "-v", "--version", type=str, required=True,
        help="Версия пакета (например, 1.0.0)"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=DEFAULT_OUTPUT,
        help=f"Имя сгенерированного файла с изображением (по умолчанию: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "-d", "--max-depth", type=int, default=DEFAULT_DEPTH,
        help=f"Максимальная глубина анализа (по умолчанию: {DEFAULT_DEPTH})"
    )
    
    return parser.parse_args()

def main() -> None:
    """Точка входа в приложение."""
    args = parse_args()
    
    try:
        validate_args(args)
    except ValueError as error:
        print(f"Ошибка валидации: {error}", file=sys.stderr)
        sys.exit(1)
        
    print_config(args)
    print("Этап 1 успешно выполнен. Параметры валидны.")

if __name__ == "__main__":
    main()