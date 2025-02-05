import os
import click
from enum import Enum

class FilePath(Enum):
    CONFIG_FILE = "moku_config.json"
    CONTENT_DIR = "content"
    TEMPLATE_DIR = "templates"
    OUTPUT_DIR = "output"

    @property
    def cwd_path(self) -> str:
        base_dir = os.getcwd()
        return os.path.join(base_dir, self.value)

    @property
    def project_path(self) -> str:
        module_path = os.path.abspath(__file__)
        project_dir = os.path.dirname(module_path)
        return os.path.join(project_dir, self.value)

def write_error_msg(error_msg: str):
    click.secho(f"Error: {error_msg} :/", fg="red")

def write_warning_msg(warning_msg: str):
    click.secho(f"Warning: {warning_msg} :/", fg="yellow")
