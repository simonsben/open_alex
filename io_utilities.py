from json import load, dump
from pathlib import Path
from typing import NoReturn, Union
from functools import partial

config_path = Path("config.json")


def save_json(path: Path, data: Union[dict, list]) -> NoReturn:
    """Stringify and write json data to file"""
    with path.open("w") as fl:
        dump(data, fl)


def load_json(path: Path) -> Union[dict, list]:
    """Load and parse json from file"""
    with path.open() as fl:
        return load(fl)


load_config = partial(load_json, path=config_path)
