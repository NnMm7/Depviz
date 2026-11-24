"""Обход графа зависимостей (DFS с рекурсией)."""

from dataclasses import dataclass, field
from graph import Graph


@dataclass
class TraversalResult:
    """Результат обхода."""
    order: list[str] = field(default_factory=list)
    cycles: list[tuple[str, str]] = field(default_factory=list)


def traverse_dfs(
    graph: Graph,
    root: str,
    max_depth: int,
    exclude_substring: str | None = None,
) -> TraversalResult:
    """Обходит граф DFS с рекурсией, с учётом глубины и циклов."""
    result = TraversalResult()
    if root not in graph.adjacency:
        return result
    visited: set[str] = set()
    stack: set[str] = set()
    _dfs(graph, root, 0, max_depth, exclude_substring, visited, stack, result)
    return result


def _is_excluded(name: str, exclude_substring: str | None) -> bool:
    """Проверяет, нужно ли исключить узел."""
    if not exclude_substring:
        return False
    return exclude_substring in name


def _dfs(
    graph: Graph,
    name: str,
    depth: int,
    max_depth: int,
    exclude_substring: str | None,
    visited: set[str],
    stack: set[str],
    result: TraversalResult,
) -> None:
    """Рекурсивная часть обхода."""
    if _is_excluded(name, exclude_substring):
        return
    if depth > max_depth:
        return
    if name in stack:
        result.cycles.append((name, name))
        return
    if name in visited:
        return
    visited.add(name)
    stack.add(name)
    result.order.append(name)
    for child in graph.children(name):
        _dfs(
            graph, child, depth + 1, max_depth,
            exclude_substring, visited, stack, result,
        )
    stack.discard(name)