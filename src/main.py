"""Depviz — визуализатор графа зависимостей.

Этап 2: поддержка локального репозитория (--repo) и генерация
DOT-файла (--graphviz) с фильтрацией зависимостей (--filter).
"""
import argparse
import os
import re
import sys


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="depviz",
        description="Визуализатор графа зависимостей пакета.",
    )
    parser.add_argument(
        "--graphviz",
        required=True,
        help="Путь к выходному DOT-файлу (Graphviz).",
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Путь к локальному репозиторию (папке с requirements.txt).",
    )
    parser.add_argument(
        "--package",
        default=None,
        help="Имя анализируемого пакета (необязательно).",
    )
    parser.add_argument(
        "--filter",
        default=".*",
        help="Регулярное выражение для фильтрации имён зависимостей.",
    )
    return parser.parse_args(argv)


def read_requirements(repo_path):
    """Читает requirements.txt из локального репозитория и возвращает список зависимостей."""
    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Репозиторий не найден: {repo_path}")

    req_file = os.path.join(repo_path, "requirements.txt")
    if not os.path.isfile(req_file):
        raise FileNotFoundError(f"В репозитории нет requirements.txt: {req_file}")

    deps = []
    with open(req_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # отбрасываем версии и маркеры: "requests>=2.0" -> "requests"
            name = re.split(r"[<>=!~;\[ ]", line, maxsplit=1)[0].strip()
            if name:
                deps.append(name)
    return deps


def filter_deps(deps, pattern):
    """Оставляет зависимости, чьё имя удовлетворяет регулярному выражению."""
    regex = re.compile(pattern)
    return [d for d in deps if regex.search(d)]


def build_dot(package, deps):
    """Строит текст DOT-графа: package -> dep1, dep2, ..."""
    lines = ["digraph dependencies {", '    rankdir="LR";']
    if package:
        lines.append(f'    "{package}";')
        for dep in deps:
            lines.append(f'    "{package}" -> "{dep}";')
    else:
        # если имя пакета не задано — просто перечисляем зависимости
        for dep in deps:
            lines.append(f'    "{dep}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def main(argv=None):
    args = parse_args(argv)

    try:
        deps = read_requirements(args.repo)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    deps = filter_deps(deps, args.filter)
    dot = build_dot(args.package, deps)

    out_dir = os.path.dirname(os.path.abspath(args.graphviz))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(args.graphviz, "w", encoding="utf-8") as f:
        f.write(dot)

    print(f"Граф зависимостей сохранён в {args.graphviz} "
          f"(зависимостей: {len(deps)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())