from typer.testing import CliRunner

from zamery_education_v4.cli.app import app


def test_explain_gate_repair_golden_and_release_groups_are_exposed() -> None:
    runner = CliRunner()
    for group in ("explain", "gate", "repair", "golden", "release"):
        result = runner.invoke(app, [group, "--help"])
        assert result.exit_code == 0, result.output
