import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]


def invoke(command: list[str], output_dir: Path) -> dict:
    invocation = {"protocol_version":"zamery-capability.v1","invocation_id":"parity","capability_id":"reference","capability_version":"4.0.0","input_records":[],"configuration":{},"input_mount":str(output_dir.parent / "inputs"),"output_mount":str(output_dir)}
    output_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(command, input=json.dumps(invocation), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def test_cross_language_hash_parity(tmp_path: Path) -> None:
    py = invoke([sys.executable, str(ROOT / "capabilities/reference/python_echo/main.py")], tmp_path / "py")
    node = invoke(["node", str(ROOT / "capabilities/reference/node_echo/main.mjs")], tmp_path / "node")
    assert py["outputs"][0]["declared_hash"] == node["outputs"][0]["declared_hash"]
