import tomli
import pathlib
from box import Box

import paths


def load_settings(settings_path=None) -> Box:
    if not settings_path:
        settings_path = paths.get_working_directory_path() + r"\settings.toml"

    with open(settings_path, 'rb') as f:
        settings_data = tomli.load(f)

    settings = Box(settings_data)
    return settings


def save_settings(settings, settings_path: str = None) -> None:
    if not settings_path:
        settings_path = paths.get_working_directory_path()

    with open(settings_path, 'wb') as f:
        tomli.dump(settings.to_dict(), f)
