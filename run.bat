@echo off
python -m src.main ^
  --graphviz graph.dot ^
  --repo . ^
  --package mypkg ^
  --filter ".*" ^
  --render