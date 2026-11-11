#!/usr/bin/env bash
set -e
python -m src.main \
  --graphviz graph.dot \
  --repo . \
  --package mypkg \
  --filter ".*"