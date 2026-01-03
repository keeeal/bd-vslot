from pathlib import Path
from typing import Any

import pytest
import yaml

from bd_vslot import *


@pytest.fixture
def module_path() -> Path:
    return Path("src") / "bd_vslot"


@pytest.fixture
def parts_config_path(
    module_path: Path,
) -> Path:
    return module_path / "config" / "parts.yaml"


@pytest.fixture
def parts_config(
    parts_config_path: Path,
) -> dict[str, dict[str, Any]]:
    with open(parts_config_path) as f:
        return yaml.safe_load(f)


def test_parts(
    parts_config: dict[str, dict[str, Any]],
    tmp_path: Path,
):
    for name, params in parts_config.items():
        part_path = tmp_path / f"{name}.stl"
        part = globals()[name](**params)
        export_stl(part, part_path)

        try:
            assert part_path.is_file()
            assert part_path.stat().st_size > 0
        except AssertionError:
            pytest.fail(f"Screenshot failed: {name}")
