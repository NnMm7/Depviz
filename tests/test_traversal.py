"""Тесты DFS-обхода (этап 3)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from graph import Graph
from traversal import traverse_dfs

def test_traverse_order():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    result = traverse_dfs(graph, "A", max_depth=10)
    assert result.order[0] == "A"
    assert set(result.order) == {"A", "B", "C"}

def test_traverse_cycle_detected():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "A")
    result = traverse_dfs(graph, "A", max_depth=10)
    assert len(result.cycles) > 0