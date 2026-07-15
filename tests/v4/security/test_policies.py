import json
from pathlib import Path

import yaml

from zamery_education_v4.kernel.hashing import sha256_file


def test_production_network_is_fail_closed() -> None:
    policy = yaml.safe_load(
        Path("security/v4/network-allowlist.yaml").read_text()
    )
    assert policy["production_default"] == "deny"
    for path in Path("capabilities").rglob("manifest.json"):
        assert json.loads(path.read_text()).get("network_domains") != ["*"]


def test_all_capabilities_have_verified_runtime_and_lockfile_identity() -> None:
    registry = yaml.safe_load(
        Path("security/v4/runtime-digests.yaml").read_text()
    )["capabilities"]
    for path in Path("capabilities").rglob("manifest.json"):
        manifest = json.loads(path.read_text())
        capability_id = manifest["capability_id"]
        assert len(manifest["runtime_digest"]) == len("sha256:") + 64
        lockfile = Path(manifest["lockfile_path"])
        assert lockfile.is_file()
        assert sha256_file(lockfile) == manifest["lockfile_hash"]
        assert registry[capability_id]["runtime_digest"] == manifest["runtime_digest"]
        assert registry[capability_id]["lockfile_hash"] == manifest["lockfile_hash"]
        if manifest["runtime_kind"] == "node":
            assert (path.parent / "package-lock.json").exists()
