#!/bin/bash

set -e

echo "Running tests with 95% minimum coverage..."

uv run pytest --cov=app --cov=lib --cov-report=term-missing --cov-fail-under=95
