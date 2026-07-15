from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from zamery_education_v4.kernel.hashing import sha256_file

HASH_PREFIX = "sha256:"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production", action="store_true")
    parser.add_argument("--container-image")
    args = parser.parse_args()
    registry = yaml.safe_load(
        Path("security/v4/runtime-digests.yaml").read_text(encoding="utf-8")
    )["capabilities"]
    failures: list[str] = []
    manifests = sorted(Path("capabilities").rglob("manifest.json"))
    for path in manifests:
        data = json.loads(path.read_text(encoding="utf-8"))
        capability_id = data["capability_id"]
        if data.get("network_domains") == ["*"]:
            failures.append(f"{capability_id}: wildcard production network")
        for field in ("runtime_digest", "lockfile_hash"):
            value = data.get(field, "")
            if (
                not isinstance(value, str)
                or not value.startswith(HASH_PREFIX)
                or len(value) != 71
            ):
                failures.append(f"{capability_id}: invalid {field}")
        lockfile_path = data.get("lockfile_path")
        if not lockfile_path:
            failures.append(f"{capability_id}: lockfile_path missing")
        else:
            lockfile = Path(lockfile_path)
            if not lockfile.is_file():
                failures.append(f"{capability_id}: lockfile missing: {lockfile}")
            elif sha256_file(lockfile) != data.get("lockfile_hash"):
                failures.append(f"{capability_id}: lockfile hash mismatch")
        expected = registry.get(capability_id)
        if expected is None:
            failures.append(f"{capability_id}: missing runtime registry entry")
        elif (
            expected["runtime_digest"] != data["runtime_digest"]
            or expected["lockfile_hash"] != data["lockfile_hash"]
            or expected.get("lockfile_path") != data.get("lockfile_path")
        ):
            failures.append(f"{capability_id}: runtime registry mismatch")
        if data.get("runtime_kind") == "node" and not (
            path.parent / "package-lock.json"
        ).exists():
            failures.append(f"{capability_id}: Node adapter is unlocked")
    if args.production:
        image = args.container_image or ""
        if "@sha256:" not in image or len(image.rsplit("@sha256:", 1)[-1]) != 64:
            failures.append("document-tool base image must be an immutable @sha256 reference")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"verified {len(manifests)} capability manifests and lockfiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
