import click

def get_config_file_name() -> str:
    return "moku_config.json"

def write_error_msg(error_msg: str):
    click.secho(f"Error: {error_msg} :/", fg="red")
