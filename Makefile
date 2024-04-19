.PHONY: install format test lock docs clean

pip-compile-options = --quiet --upgrade --no-emit-index-url

# Install package. Usage: make install [dev=true]
install:
	pip install --upgrade pip pip-tools
	pip install -r requirements$(if $(dev),-dev,).txt
	pip install -e .

# Format code. Usage: make format [check=true]
format:
	isort $(if $(check),--check,) .
	black $(if $(check),--check,) .

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
