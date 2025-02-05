import click
import os
import json
from typing import Dict, Optional
from util import get_config_file_name, write_error_msg


@click.command()
@click.option("--name", prompt="project name", default="mywebpage",show_default=True)
def init(name: str):
    create_scaffold(project_dir=name) 

def create_scaffold(project_dir: str):
    script_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    call_path: str = os.path.join(os.getcwd(), project_dir)
    moku_config_path: str = os.path.join(script_path, get_config_file_name())

    structure = load_and_parse_config(config_path=moku_config_path)
    if structure is not None:
        process_structure(scaffold_structure=structure, current_path=call_path)

def load_and_parse_config(config_path: str) -> Optional[Dict]: 
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        write_error_msg("moku_config not present")
        return None
    except json.JSONDecodeError:
        write_error_msg("failed to parse moku_config")
        return None

    return config["scaffold_structure"]

def process_structure(scaffold_structure: Dict, current_path: str):
    for key, value in scaffold_structure.items():
        if key == "files":
            for file in value:
                create_file(path=current_path, file_name=file)
        else: 
            new_path = os.path.join(current_path, key)
            create_dir(new_path)
            process_structure(value, new_path)

def create_file(path: str, file_name: str):
    with open(os.path.join(path, file_name), "w") as new_file:
        new_file.write("")

def create_dir(path: str):
    os.makedirs(path, exist_ok=True)
