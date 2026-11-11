"""Тесты для CLI-приложения."""
import unittest
from unittest.mock import patch
from src.main import validate_args

class TestValidateArgs(unittest.TestCase):
    """Тестирование функции валидации аргументов."""

    def test_valid_args(self) -> None:
        """Тест с корректными аргументами."""
        class MockArgs:
            package = "my_package"
            repo = "https://github.com/user/repo"
            version = "1.0.0"
            max_depth = 3
            output = "graph.png"
        
        # Не должно вызывать исключений
        validate_args(MockArgs())

    def test_invalid_version(self) -> None:
        """Тест с некорректной версией."""
        class MockArgs:
            package = "my_package"
            repo = "https://github.com/user/repo"
            version = "1.0"
            max_depth = 3
            output = "graph.png"
        
        with self.assertRaises(ValueError):
            validate_args(MockArgs())

if __name__ == "__main__":
    unittest.main()