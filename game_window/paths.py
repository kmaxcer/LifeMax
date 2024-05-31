import os
import sys
from pathlib import Path


def get_resource_path(relative_path=""):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    resource_path = os.path.join(base_path, relative_path)
    return str(Path(resource_path).resolve())


def get_working_directory_path() -> str:
    return get_resource_path()