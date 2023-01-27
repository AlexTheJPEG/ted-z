import json
from pathlib import Path

import tomllib


def open_file(filename: str) -> list[str]:
    with Path(f"ted-z/files/{filename}").open("r") as file:
        return [line.strip() for line in file.readlines()]


def load_json(filename: str) -> dict:
    with Path(f"ted-z/files/{filename}").open("r") as file:
        return json.load(file)


def load_bot_settings() -> dict:
    with Path("bot_settings.toml").open("rb") as settings:
        return tomllib.load(settings)
