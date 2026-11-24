"""CLI-инструмент визуализации графа зависимостей (этап 3)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config, ConfigError, build_config, parse_args, print_config
from fetcher import FetchError, fetch_package_json
from graph import Graph
from npm_parser import extract_direct_dependencies, extract_package_name
from test_repo import TestRepoError, load_graph_from_file


def _print_dfs_tree(graph: Graph, root: str, max_depth: int, exclude: str | None = None) -> None:
    """Выводит дерево обхода в консоль."""
    print("\n=== Анализ графа зависимостей (DFS) ===")
    print(f"Стартовый узел: {root}")
    print("Обход графа:")
    visited: set[str] = set()

    def _dfs_print(node: str, depth: int, prefix: str = "") -> None:
        if depth > max_depth:
            print(f"{prefix}└── {node} (лимит глубины)")
            return
        if exclude and exclude in node and node != root:
            return
        if node in visited:
            print(f"{prefix}└── {node} (цикл/посещен)")
            return
        visited.add(node)
        print(f"{prefix}├── {node}")
        children = graph.children(node)
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)
            new_prefix = prefix + ("    " if is_last else "│   ")
            _dfs_print(child, depth + 1, new_prefix)

    _dfs_print(root, 0)
    print(f"\nОбход завершен. Всего узлов: {len(visited)}.")


def _load_graph_real(config: Config) -> Graph:
    """Загружает граф из реального package.json."""
    package_json = fetch_package_json(config.source)
    root = extract_package_name(package_json)
    graph = Graph()
    graph.add_node(root)
    for dep in extract_direct_dependencies(package_json):
        graph.add_edge(root, dep)
    return graph


def run_stage_three(config: Config) -> int:
    """Строит граф и выполняет DFS-обход."""
    print_config(config)
    try:
        if config.test_mode:
            graph = load_graph_from_file(config.source)
            if config.package not in graph.adjacency:
                graph.add_node(config.package)
        else:
            graph = _load_graph_real(config)
    except (FetchError, TestRepoError, ValueError) as error:
        print(f"Ошибка сбора данных: {error}", file=sys.stderr)
        return 4

    _print_dfs_tree(
        graph,
        root=config.package,
        max_depth=config.max_depth,
        exclude=config.package if config.test_mode else None,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    """Точка входа приложения."""
    args = parse_args(argv)
    try:
        config = build_config(args)
    except ConfigError as error:
        print(f"Ошибка конфигурации: {error}", file=sys.stderr)
        return 2
    return run_stage_three(config)


if __name__ == "__main__":
    raise SystemExit(main())