PACKAGE_NAME := organize_me
BUILD_DIR := "$(realpath)/build"
PACKAGE_VERSION := $(shell cat VERSION)

.PHONY: test bootstrap package mypy ruff format check help

# Default target
.DEFAULT_GOAL := help

run: bootstrap
	@echo "Running ..."
	@poetry run organize-me

package: bootstrap
	@echo "📦 Packaging $(PACKAGE_NAME) version $(PACKAGE_VERSION)..."
	@poetry build
	@echo "✅  Package created"

check: ruff mypy

mypy: bootstrap
	@echo "🔍 Running mypy..."
	@poetry run mypy --strict -p $(PACKAGE_NAME)
	@echo "✅ mypy passed"

ruff: bootstrap
	@echo "🔍 Running ruff..."
	@poetry run ruff check ${PACKAGE_NAME} --fix
	@echo "✅  ruff passed"

format: bootstrap
	@echo "🔍 Running ruff format..."
	@poetry run ruff format ${PACKAGE_NAME}
	@echo "✅  ruff format Done"

test: bootstrap
	@echo "🔍 Running tests..."
	@poetry run pytest --log-cli-level=4 tests
	@echo "✅  Tests passed"

bootstrap: .make.bootstrap

# We need to reinstall dependencies whenever pyproject.toml is newer than the
# lock file than the one created the last time we bootstrapped.
# We can't use the committed lock file, as it is committed to git and when
# someone pulls it from git it will always seem up to date.
.make.bootstrap: pyproject.toml
	@echo "🔧 Bootstrapping..."
	@poetry install
	@touch .make.bootstrap
	@echo "✅  Bootstrapped"

help:
	@echo "ℹ️ Available commands:"
	@echo "  run       - Run the project"
	@echo "  bootstrap - Install dependencies"
	@echo "  test      - Run tests"
	@echo "  package   - package the project"
	@echo "  mypy      - Run mypy"
	@echo "  ruff      - Run ruff"
	@echo "  format    - Run ruff format"
	@echo "  check     - Run ruff and mypy"
	@echo "  help      - Show this help message"