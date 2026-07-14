from __future__ import annotations

import json
import sys
from pathlib import Path

SUPPORTED_FORMATS = {
    "docx", "pdf", "pptx", "html", "tsv", "csv", "jsonl", "sqlite", "qti", "h5p"
}
STRUCTURED_FORMATS = {"jsonl", "sqlite", "qti", "h5p"}
BLOCKING_SAFETY_KINDS = {"pii", "answer_leakage"}


def validate_pack_manifest(data: dict[str, object]) -> list[str]:
    """Validate pack identity, objective lineage, dependencies, answers, brand, and formats."""
    errors: list[str] = []
    for field in ("pack_id", "brief_id"):
        if not isinstance(data.get(field), str) or not str(data[field]).strip():
            errors.append(f"{field} must be a non-empty string")

    declared = data.get("objective_ids")
    known_objectives = {
        value for value in declared if isinstance(value, str) and value.strip()
    } if isinstance(declared, list) else set()
    if not known_objectives:
        errors.append("objective_ids must be a non-empty string list")

    formats = data.get("requested_formats")
    if not isinstance(formats, list) or not formats:
        errors.append("requested_formats must be a non-empty list")
    else:
        for requested in formats:
            if requested not in SUPPORTED_FORMATS:
                errors.append(f"unsupported requested format {requested}")

    brand = data.get("brand")
    if not isinstance(brand, dict):
        errors.append("brand must be an object")
    else:
        if brand.get("name") != "zamery" or brand.get("tagline") != "rooted in strength":
            errors.append("brand name and tagline must match the supplied Zamery identity")
        if brand.get("design_system") != "zamery-core.v2":
            errors.append("brand design_system must be zamery-core.v2")

    verification = data.get("delivery_verification")
    if not isinstance(verification, dict):
        errors.append("delivery_verification must be an object")
    else:
        for field in ("crc_checked", "reextracted", "nested_ooxml_checked", "rerendered_from_extracted"):
            if verification.get(field) is not True:
                errors.append(f"delivery verification requires {field}")
        if isinstance(formats, list) and STRUCTURED_FORMATS.intersection(formats):
            if verification.get("structured_exports_checked") is not True:
                errors.append("delivery verification requires structured_exports_checked")

    findings = data.get("safety_findings")
    if not isinstance(findings, list):
        errors.append("safety_findings must be a list")
    else:
        for finding in findings:
            if not isinstance(finding, dict) or finding.get("kind") not in BLOCKING_SAFETY_KINDS:
                continue
            errors.append(
                "blocking safety finding "
                f"{finding['kind']} in {finding.get('artifact_id', 'unknown')}: "
                f"{finding.get('detail', 'no detail')}"
            )

    artifacts = data.get("artifacts")
    artifact_by_id: dict[str, dict[str, object]] = {}
    artifact_ids: list[str] = []
    covered_objectives: set[str] = set()
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must be a non-empty list")
        return errors

    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            errors.append(f"artifact {index} must be an object")
            continue
        artifact_id = artifact.get("artifact_id")
        if not isinstance(artifact_id, str) or not artifact_id.strip():
            errors.append(f"artifact {index} requires a non-empty artifact_id")
            continue
        artifact_ids.append(artifact_id)
        artifact_by_id[artifact_id] = artifact
        version = artifact.get("version")
        if isinstance(version, bool) or not isinstance(version, int) or version < 1:
            errors.append(f"artifact {artifact_id} version must be a positive integer")
        refs = artifact.get("objective_ids")
        if not isinstance(refs, list) or not refs:
            errors.append(f"artifact {artifact_id} requires objective_ids")
        else:
            for objective_id in refs:
                if objective_id not in known_objectives:
                    errors.append(f"artifact {artifact_id} cites unknown objective {objective_id}")
                else:
                    covered_objectives.add(str(objective_id))

    if len(artifact_ids) != len(set(artifact_ids)):
        errors.append("artifact IDs must be unique")
    for objective_id in declared if isinstance(declared, list) else []:
        if objective_id not in covered_objectives:
            errors.append(f"pack objective {objective_id} is not covered by any artifact")

    for artifact_id in artifact_ids:
        artifact = artifact_by_id[artifact_id]
        dependencies = artifact.get("dependencies", [])
        if not isinstance(dependencies, list):
            errors.append(f"artifact {artifact_id} dependencies must be a list")
            continue
        for dependency in dependencies:
            if not isinstance(dependency, dict):
                errors.append(f"artifact {artifact_id} has an invalid dependency")
                continue
            dependency_id = dependency.get("artifact_id")
            current = artifact_by_id.get(str(dependency_id))
            if current is None:
                errors.append(f"artifact {artifact_id} depends on missing {dependency_id}")
            elif dependency.get("version") != current.get("version"):
                errors.append(
                    f"artifact {artifact_id} depends on stale {dependency_id} "
                    f"version {dependency.get('version')}; current is {current.get('version')}"
                )

        if artifact.get("artifact_type") == "answer_set":
            if artifact.get("audience") != "teacher":
                errors.append(f"answer_set {artifact_id} must be teacher-only")
            source_id = artifact.get("source_artifact_id")
            source = artifact_by_id.get(str(source_id))
            if source is None or source.get("artifact_type") == "answer_set":
                errors.append(f"answer_set {artifact_id} requires an existing non-answer source")
            elif artifact.get("source_version") != source.get("version"):
                errors.append(f"answer_set {artifact_id} source version is stale")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_pack_manifest.py PACK.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate_pack_manifest(data)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
