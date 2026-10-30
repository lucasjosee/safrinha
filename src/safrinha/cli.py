from importlib.metadata import version as package_version

import typer

app = typer.Typer(no_args_is_help=True)


# With a single command, Typer would run it as the whole program and
# `safrinha version` would fail. The callback keeps subcommand mode.
@app.callback()
def main() -> None:
    """Safrinha: soybean and corn management assistant."""


@app.command()
def version() -> None:
    """Show the installed version."""
    typer.echo(f"safrinha {package_version('safrinha')}")
