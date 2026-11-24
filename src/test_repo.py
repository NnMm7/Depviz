"""Загрузчик тестового репозитория из файла-описания графа.

Формат: строки вида "A B C" означают рёбра A->B, A->C.
Пакеты — большие латинские буквы.
"""

from graph import Graph


class TestRepoError(ValueError):
    """Ошибка разбора файла-описания графа."""


def load_graph_from_file(path: str) -> Graph:
    """Строит граф из текстового файла."""
    graph = Graph()
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            _parse_line(graph, line, line_number, path)
    return graph


def _parse_line(graph: Graph, line: str, line_number: int, path: str) -> None:
    """Разбирает одну строку файла."""
    tokens = line.split()
    if len(tokens) < 2:
        raise TestRepoError(
            f"{path}:{line_number}: ожидается родитель и хотя бы один потомок."
        )
    for token in tokens:
        if not token.isalpha() or not token.isupper():
            raise TestRepoError(
                f"{path}:{line_number}: имя пакета должно быть большими "
                f"латинскими буквами, получено {token!r}."
            )
    parent, *children = tokens
    graph.add_node(parent)
    for child in children:
        graph.add_edge(parent, child)