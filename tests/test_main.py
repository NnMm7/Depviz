"""Модульные тесты для depviz (этап 3)."""
import os
import tempfile
import unittest
from unittest.mock import patch

from src.main import (
    parse_args,
    read_requirements,
    filter_deps,
    build_dot,
    render_png,
    main,
)


class TestParseArgs(unittest.TestCase):
    def test_all_args(self):
        args = parse_args([
            "--graphviz", "out.dot",
            "--repo", "/tmp/repo",
            "--package", "mypkg",
            "--filter", "^req",
            "--render",
        ])
        self.assertEqual(args.graphviz, "out.dot")
        self.assertEqual(args.repo, "/tmp/repo")
        self.assertEqual(args.package, "mypkg")
        self.assertEqual(args.filter, "^req")
        self.assertTrue(args.render)


class TestReadRequirements(unittest.TestCase):
    def test_simple(self):
        with tempfile.TemporaryDirectory() as repo:
            with open(os.path.join(repo, "requirements.txt"), "w", encoding="utf-8") as f:
                f.write("# comment\nrequests>=2.0\nflask==1.0\n\n")
            self.assertEqual(read_requirements(repo), ["requests", "flask"])


class TestRenderPng(unittest.TestCase):
    @patch("shutil.which", return_value="/usr/bin/dot")
    @patch("subprocess.run")
    def test_render_success(self, mock_run, mock_which):
        # Мокаем subprocess.run, чтобы не вызывать реальный Graphviz
        self.assertTrue(render_png("graph.dot"))
        mock_run.assert_called_once_with(
            ["dot", "-Tpng", "graph.dot", "-o", "graph.png"], check=True
        )

    @patch("shutil.which", return_value=None)
    def test_render_no_dot(self, mock_which):
        # Если dot не установлен, функция должна вернуть False
        self.assertFalse(render_png("graph.dot"))


class TestMain(unittest.TestCase):
    @patch("src.main.render_png")
    def test_main_render_flag(self, mock_render):
        with tempfile.TemporaryDirectory() as repo:
            with open(os.path.join(repo, "requirements.txt"), "w", encoding="utf-8") as f:
                f.write("requests\n")
            out = os.path.join(repo, "g.dot")
            
            # Вызов с флагом --render
            rc = main(["--graphviz", out, "--repo", repo, "--render"])
            self.assertEqual(rc, 0)
            mock_render.assert_called_once_with(out)


if __name__ == "__main__":
    unittest.main()