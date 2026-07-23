#!/bin/bash
set -e

echo "======== Styling (ruff) =========="
ruff check
echo ""

echo "========= Linting (ruff) ========="
ruff format --check
echo ""

echo "======= Testing (pytest) ======="
pytest
echo ""
