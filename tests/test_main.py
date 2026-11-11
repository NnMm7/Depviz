"""Модульные тесты для depviz (этап 2)."""
import os
import tempfile
import unittest
from unittest.mock import patch

from src.main import (
    parse_args,
    read_requirements,
    filter_deps,
    build_dot,
    main,
)


class TestParseArgs(unittest.TestCase):
    def test_all_args(self):
        args = parse_args([
            "--graphviz", "out.dot",
            "--repo", "/tmp/repo",
            "--package", "mypkg",
            "--filter", "^req",
        ])
        self.assertEqual(args.graphviz, "out.dot")
        self.assertEqual(args.repo, "/tmp/repo")
        self.assertEqual(args.package, "mypkg")
        self.assertEqual(args.filter, "^req")

    def test_filter_default(self):
        args = parse_args(["--graphviz", "g.dot", "--repo", "."])
        self.assertEqual(args.filter, ".*")
        self.assertIsNone(args.package)

    def test_missing_required(self):
        with self.assertRaises(SystemExit):
            with patch("sys.stderr"):
                parse_args([])


class TestReadRequirements(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, content):
        with open(os.path.join(self.repo, "requirements.txt"), "w", encoding="utf-8") as f:
            f.write(content)

    def test_simple(self):
        self._write("requests\nflask\n")
        self.assertEqual(read_requirements(self.repo), ["requests", "flask"])

    def test_versions_and_comments(self):
        self._write("# comment\nrequests>=2.0\nflask==1.0\n\n")
        self.assertEqual(read_requirements(self.repo), ["requests", "flask"])

    def test_missing_repo(self):
        with self.assertRaises(FileNotFoundError):
            read_requirements(os.path.join(self.repo, "nope"))

    def test_missing_requirements(self):
        with self.assertRaises(FileNotFoundError):
            read_requirements(self.repo)


class TestFilterDeps(unittest.TestCase):
    def test_filter(self):
        deps = ["requests", "flask", "numpy"]
        self.assertEqual(filter_deps(deps, "^req"), ["requests"])
        self.assertEqual(filter_deps(deps, ".*"), deps)
        self.assertEqual(filter_deps(deps, "^z"), [])


class TestBuildDot(unittest.TestCase):
    def test_with_package(self):
        dot = build_dot("mypkg", ["requests", "flask"])
        self.assertIn('"mypkg" -> "requests";', dot)
        self.assertIn('"mypkg" -> "flask";', dot)
        self.assertTrue(dot.startswith("digraph dependencies {"))
        self.assertTrue(dot.rstrip().endswith("}"))

    def test_without_package(self):
        dot = build_dot(None, ["requests"])
        self.assertIn('"requests";', dot)
        self.assertNotIn("->", dot)


class TestMainEndToEnd(unittest.TestCase):
    def test_writes_dot_file(self):
        with tempfile.TemporaryDirectory() as repo:
            with open(os.path.join(repo, "requirements.txt"), "w", encoding="utf-8") as f:
                f.write("requests\nflask\n")
            out = os.path.join(repo, "graph.dot")
            rc = main([
                "--graphviz", out,
                "--repo", repo,
                "--package", "mypkg",
                "--filter", ".*",
            ])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(out))
            with open(out, encoding="utf-8") as f:
                content = f.read()
            self.assertIn('"mypkg" -> "requests";', content)
            self.assertIn('"mypkg" -> "flask";', content)


if __name__ == "__main__":
    unittest.main()