"""Модель графа зависимостей."""

from dataclasses import dataclass, field


@dataclass
class Graph:
    """Направленный граф зависимостей."""

    adjacency: dict[str, list[str]] = field(default_factory=dict)

    def add_node(self, name: str) -> None:
        """Добавляет узел, если его ещё нет."""
        self.adjacency.setdefault(name, [])

    def add_edge(self, parent: str, child: str) -> None:
        """Добавляет ребро parent -> child."""
        self.add_node(parent)
        self.add_node(child)
        if child not in self.adjacency[parent]:
            self.adjacency[parent].append(child)

    def children(self, name: str) -> list[str]:
        """Возвращает список прямых зависимостей узла."""
        return list(self.adjacency.get(name, []))