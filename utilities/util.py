import os
import click
from enum import Enum

class FilePath(Enum):
    CONFIG_FILE = "../moku_config.json"
    TEMPLATE_DIR = "../templates"
    CONTENT_DIR = "content"
    POSTS_DIR = str(os.path.join(CONTENT_DIR, "posts"))
    OUTPUT_DIR = "output"
    OUTPUT_POSTS = str(os.path.join(OUTPUT_DIR, "posts"))
    STATIC_DIR = "static"
    ASSETS_DIR = "static/assets"

    @property
    def cwd_path(self) -> str:
        base_dir = os.getcwd()
        return os.path.join(base_dir, self.value)

    @property
    def project_path(self) -> str:
        module_path = os.path.abspath(__file__)
        project_dir = os.path.dirname(module_path)
        return os.path.join(project_dir, self.value)


def is_moku_project_dir() -> bool:
    return os.path.isfile(os.path.join(os.getcwd(), ".moku"))

def write_error_msg(error_msg: str):
    click.secho(f"Error: {error_msg} :/", fg="red")

def write_warning_msg(warning_msg: str):
    click.secho(f"Warning: {warning_msg} :/", fg="yellow")
