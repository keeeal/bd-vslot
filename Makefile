.PHONY: lock docs

pip-compile-options = --quiet --upgrade --no-emit-index-url

# Lock all requirements
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
