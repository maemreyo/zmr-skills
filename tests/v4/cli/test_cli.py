from typer.testing import CliRunner

from zamery_education_v4.cli.app import app


def test_help_lists_required_groups() -> None:
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("graph", "plan", "run", "resume", "impact", "index", "cache"):
        assert command in result.stdout
