from pathlib import Path
from subprocess import run
from typing import Any

import pytest
import yaml


@pytest.fixture
def docs_path() -> Path:
    return Path("docs")


@pytest.fixture
def screenshots_script_path(
    docs_path: Path,
) -> Path:
    return docs_path / "screenshots.py"


@pytest.fixture
def screenshots_config_path(
    docs_path: Path,
) -> Path:
    return docs_path / "screenshots.yaml"


@pytest.fixture
def screenshots_config(
    screenshots_config_path: Path,
) -> dict[str, dict[str, Any]]:
    with open(screenshots_config_path) as f:
        return yaml.safe_load(f)


def test_screenshots(
    screenshots_script_path: Path,
    screenshots_config: dict[str, dict[str, Any]],
    tmp_path: Path,
):
    run(
        ["python", screenshots_script_path.as_posix(), "-o", tmp_path.as_posix()],
        check=True,
    )

    for name in screenshots_config.keys():
        screenshot_path = tmp_path / f"{name}.png"
        try:
            assert screenshot_path.is_file()
            assert screenshot_path.stat().st_size > 0
        except AssertionError:
            pytest.fail(f"Screenshot failed: {screenshot_path.as_posix()}")
