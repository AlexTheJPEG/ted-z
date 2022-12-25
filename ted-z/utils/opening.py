import json

import tomli


def open_file(filename):
    with open(f"ted-z/files/{filename}", "r") as file:
        return [line.strip() for line in file.readlines()]


def load_json(filename):
    with open(f"ted-z/files/{filename}", "r") as file:
        return json.load(file)


def load_bot_settings():
    with open("bot_settings.toml", "rb") as settings:
        return tomli.load(settings)
