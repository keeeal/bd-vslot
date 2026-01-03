# Requires dev dependencies to be installed:
# > make install dev=true

from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import yaml
from ocp_vscode import save_screenshot, show  # type: ignore[import-untyped]

from bd_vslot import *


def save_screenshots(
    config: Path,
    output: Path,
):
    with open(config) as f:
        data: dict[str, dict[str, Any]] = yaml.safe_load(f)

    output.mkdir(parents=True, exist_ok=True)

    for name, params in data.items():
        part = globals()[name](**params)
        show(part)
        save_screenshot((output / f"{name}.png").as_posix())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--config", type=Path, default=Path("src/bd_vslot/config/parts.yaml")
    )
    parser.add_argument("-o", "--output", type=Path, default=Path("docs/screenshots"))
    save_screenshots(**vars(parser.parse_args()))
