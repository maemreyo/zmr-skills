from pathlib import Path
from zamery_education_v4.kernel.records.context import TeachingBrief
from zamery_education_v4.kernel.storage import RecordStore, StoreLayout, rebuild_index

def test_deleted_index_rebuilds_to_same_fingerprint(tmp_path: Path) -> None:
 layout=StoreLayout(tmp_path); store=RecordStore(layout.root); store.commit(TeachingBrief(record_id="brief:x",duration_minutes=90,learner_level="A2",source_ids=("source:x",)))
 first=rebuild_index(layout.index_path,store,()); layout.index_path.unlink(); second=rebuild_index(layout.index_path,store,())
 assert first == second

import os
import subprocess
import sys


def test_clean_index_script_creates_output_parent(tmp_path: Path) -> None:
 output = tmp_path / "nested" / "index.json"
 env = dict(os.environ, PYTHONPATH="src:.")
 result = subprocess.run(
  [sys.executable, "scripts/v4/verify_clean_index_rebuild.py", "--fixture", "unit1-lesson1", "--output", str(output)],
  cwd=Path(__file__).parents[3], env=env, capture_output=True, text=True, check=False,
 )
 assert result.returncode == 0, result.stderr
 assert output.is_file()
