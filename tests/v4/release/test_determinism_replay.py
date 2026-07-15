from pathlib import Path
from zamery_education_v4.testing import GoldenRunner

def test_two_clean_logical_runs_have_identical_graph_and_semantics() -> None:
    left=GoldenRunner().run_production("unit1-lesson1"); right=GoldenRunner().run_production("unit1-lesson1")
    assert left.graph_hash == right.graph_hash and left.gate_decisions == right.gate_decisions and left.deliverables == right.deliverables

import os
import subprocess
import sys


def test_determinism_script_creates_output_parent(tmp_path: Path) -> None:
    output = tmp_path / "nested" / "determinism.json"
    env = dict(os.environ, PYTHONPATH="src:.")
    result = subprocess.run(
        [
            sys.executable,
            "scripts/v4/run_determinism_replay.py",
            "--fixture",
            "unit1-lesson1",
            "--output",
            str(output),
        ],
        cwd=Path(__file__).parents[3],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert output.is_file()
