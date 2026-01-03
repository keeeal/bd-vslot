.PHONY: install format lint test lock docs clean

# Usage: make install [dev=true][docs=true]
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .
	$(if $(dev),pip install -e .[dev])
	$(if $(docs),pip install -e .[docs])

# Usage: make format [check=true]
format:
	isort $(if $(check),--check,) .
	black $(if $(check),--check,) .

# Type checking
lint:
	mypy .

# Run unit tests
test:
	pytest .

# Lock requirements
lock:
	pip-compile \
		--quiet \
		--upgrade \
		--no-emit-index-url \
		--output-file requirements.txt \
		pyproject.toml

screenshots:
	python docs/save_screenshots.py

# Build documentation
docs:
	sphinx-build -M html docs docs/_build

# Remove files not under version control
clean:
	git clean -Xdf
