import click
from commands.init import init
from commands.build import build
from commands.serve import serve

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.secho("""

        ╋╋╋╋╋┏┓
        ┏━━┳━┫┣┳┳┓
        ┃┃┃┃╋┃━┫┃┃
        ┗┻┻┻━┻┻┻━┛
                    """, fg="bright_blue")
        click.secho("""
        A simple and lightweight static site generator.

        Commands:
        """, fg="bright_blue")
        click.secho("         ⬡ init         ", fg="bright_magenta", nl=False)
        click.secho("--scaffold new project in the current directory", fg="bright_black")
        click.secho("         ⬡ serve        ", fg="bright_magenta", nl=False)
        click.secho("--start preview server", fg="bright_black")
        click.secho("         ⬡ build        ", fg="bright_magenta", nl=False)
        click.secho("--generate the static page", fg="bright_black")
        click.secho("         ⬡ new-post     ", fg="bright_magenta", nl=False)
        click.secho("--create new post\n", fg="bright_black")
        click.secho("        Inspired by mokuhanga (木版画), the traditional Japanese art of woodblock printing.\n\n", fg="bright_blue")

cli.add_command(init)
cli.add_command(build)
cli.add_command(serve)

@cli.command()
def new_post():
    """Create new post"""
    pass

if __name__ == '__main__':
    cli()
