from importlib.metadata import version

from typer.testing import CliRunner

from safrinha.cli import app

runner = CliRunner()


def test_version_prints_installed_version() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == f"safrinha {version('safrinha')}"
