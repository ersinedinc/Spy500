from pathlib import Path
from functools import lru_cache

import yaml


CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_yaml_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


@lru_cache()
def get_config() -> dict:
    return load_yaml_config()
