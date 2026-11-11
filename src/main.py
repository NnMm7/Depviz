"""Depviz — визуализатор графа зависимостей (Этап 3)."""
import argparse
import os
import re
import shutil
import subprocess
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
    parser.add_argument(
        "--render",
        action="store_true",
        help="Отрендерить граф в PNG с помощью утилиты dot.",
    )
    return parser.parse_args(argv)


def read_requirements(repo_path):
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
            name = re.split(r"[<>=!~;\[ ]", line, maxsplit=1)[0].strip()
            if name:
                deps.append(name)
    return deps


def filter_deps(deps, pattern):
    regex = re.compile(pattern)
    return [d for d in deps if regex.search(d)]


def build_dot(package, deps):
    lines = ["digraph dependencies {", '    rankdir="LR";']
    if package:
        lines.append(f'    "{package}";')
        for dep in deps:
            lines.append(f'    "{package}" -> "{dep}";')
    else:
        for dep in deps:
            lines.append(f'    "{dep}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_png(dot_file):
    """Вызывает утилиту dot для рендеринга графа в PNG."""
    if not shutil.which("dot"):
        print("Ошибка: утилита 'dot' не найдена. Установите Graphviz.", file=sys.stderr)
        return False
    
    png_file = os.path.splitext(dot_file)[0] + ".png"
    try:
        subprocess.run(["dot", "-Tpng", dot_file, "-o", png_file], check=True)
        print(f"Изображение графа сохранено в {png_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при рендеринге: {e}", file=sys.stderr)
        return False


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

    print(f"Граф зависимостей сохранён в {args.graphviz} (зависимостей: {len(deps)})")

    if args.render:
        if not render_png(args.graphviz):
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())