import re
from pathlib import Path
from typer.testing import CliRunner
from zamery_education_v4.cli.app import app

def test_operator_documented_cli_groups_exist() -> None:
 text=Path("docs/operations/education-v4/operator-guide.md").read_text()
 commands=re.findall(r"```bash testable\n(.*?)\n```",text,re.S)
 runner=CliRunner()
 for command in commands:
  parts=command.strip().split()[1:]
  result=runner.invoke(app,parts)
  assert result.exit_code == 0, (command,result.output)
