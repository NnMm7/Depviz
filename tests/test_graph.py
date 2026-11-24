"""Тесты модели графа (этап 3)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from graph import Graph

def test_add_edge_creates_nodes():
    graph = Graph()
    graph.add_edge("A", "B")
    assert set(graph.adjacency.keys()) == {"A", "B"}
    assert graph.children("A") == ["B"]

def test_add_edge_deduplicates():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "B")
    assert graph.children("A") == ["B"]