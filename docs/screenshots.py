from argparse import ArgumentParser
from pathlib import Path

import yaml
from ocp_vscode import save_screenshot, show

from bd_vslot import *


def main(
    config: Path,
    output: Path,
):
    with open(config) as f:
        data = yaml.safe_load(f)

    output.mkdir(parents=True, exist_ok=True)

    for name, params in data.items():
        part = globals()[name](**params)
        show(part)
        save_screenshot((output / f"{name}.png").as_posix())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--config", type=Path, default=Path("docs/screenshots.yaml")
    )
    parser.add_argument("-o", "--output", type=Path, default=Path("docs/screenshots"))
    main(**vars(parser.parse_args()))
