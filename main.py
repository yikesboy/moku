import click
import time

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

@cli.command()
def init():
    """Scaffold new project in current directory"""
    pass

@cli.command()
@click.option("--port", default=8000, help="Port to serve the site")
def serve(port):
    """Start preview server"""
    click.secho(f"Serving on http://localhost:{port}", fg="bright_blue")
    pass

@cli.command()
def build():
    """Generate the static page"""
    click.secho("\nStarting build.\n", fg='bright_blue', bold=True)
    total = 100
    with click.progressbar(range(total), label=click.style('Building', fg='bright_blue', bold=True), fill_char='█', empty_char='-', width=50) as bar:
        for _ in bar:
            time.sleep(0.03)

    click.secho("\nBuild Complete!", fg='bright_blue', bold=True)
    pass

@cli.command()
def new_post():
    """Create new post"""
    pass

if __name__ == '__main__':
    cli()
