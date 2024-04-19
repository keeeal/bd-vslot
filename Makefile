.PHONY: install format test lock docs clean

pip-compile-options = --quiet --upgrade --no-emit-index-url

# Usage: make install [dev=true]
install:
	pip install --upgrade pip pip-tools
	pip install -r requirements$(if $(dev),-dev,).txt
	pip install -e .

# Format code
format:
	isort .
	black .

# Lint code
lint:
	isort --check .
	black --check .
	mypy .

# Run unit tests
test:
	pytest .

# Lock requirements
lock:
	pip-compile \
		$(pip-compile-options) \
		--output-file requirements.txt \
		pyproject.toml
	pip-compile \
		$(pip-compile-options) \
		--extra dev \
		--output-file requirements-dev.txt \
		pyproject.toml

# Build documentation
docs:
	sphinx-build -M html docs docs/_build

# Remove files not under version control
clean:
	git clean -Xdf
