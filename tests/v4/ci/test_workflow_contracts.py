from pathlib import Path
import yaml

def test_workflows_pin_required_toolchains_and_do_not_reuse_sqlite() -> None:
 setup=Path(".github/actions/setup-education-v4/action.yml").read_text()
 assert 'python-version: "3.12"' in setup and 'node-version: "22"' in setup and "uv sync --extra dev" in setup
 texts=[]
 for path in Path(".github/workflows").glob("education-v4-*.yml"):
  text=path.read_text(); yaml.safe_load(text); texts.append(text)
 assert any("v4-determinism" in text for text in texts)
 assert all("graph.sqlite" not in text for text in texts)
 assert all("upload-artifact" in text for text in texts)
