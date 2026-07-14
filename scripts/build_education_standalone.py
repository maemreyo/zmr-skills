#!/usr/bin/env python3
"""Build self-contained ChatGPT/Codex packages for all Education skills.

The source tree keeps ``skills/education/_shared`` as the canonical copy. This
builder vendors that shared runtime into every generated skill, rewrites all
monorepo-only references/imports, certifies each package in isolation, and
creates both per-skill ZIPs and a suite ZIP.

Python 3.9+; standard library only.
"""
from __future__ import annotations

import argparse
import py_compile
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

PROMOTED_SKILL_PREFIX = "zamery-"
TEXT_EXTENSIONS = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".jsonl",
    ".md",
    ".mjs",
    ".py",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}
RUNTIME_EXCLUDED_DIRS = {"__pycache__", ".pytest_cache", "tests", "evals"}
RUNTIME_EXCLUDED_FILES = {".DS_Store"}
FORBIDDEN_STANDALONE_PATTERNS = {
    "skills.education._shared": "monorepo Python import",
    "parents[4]": "repo-root bootstrap",
}
SHARED_PATH_RE = re.compile(
    r"(?P<path>(?:\.\./)*_shared/[A-Za-z0-9_./-]*[A-Za-z0-9_-])"
)
FRONTMATTER_NAME_RE = re.compile(r"^name:\s*(?P<name>[^\s#]+)\s*$", re.MULTILINE)
MONOREPO_IMPORT_RE = re.compile(r"(?m)^from\s+skills\.education\._shared(?P<suffix>(?:\.[A-Za-z_][A-Za-z0-9_]*)?)\s+import\s+")
REPO_ROOT_ASSIGN_RE = re.compile(
    r"(?m)^_REPO_ROOT\s*=\s*Path\(__file__\)\.resolve\(\)\.parents\[4\]\s*\n"
)
REPO_ROOT_INSERT_RE = re.compile(
    r"(?m)^sys\.path\.insert\(0,\s*str\(_REPO_ROOT\)\)\s*\n"
)


@dataclass(frozen=True)
class BuildResult:
    skill_name: str
    package_dir: Path
    zip_path: Path
    file_count: int
    sha256: str


class BuildError(RuntimeError):
    """Raised when a source or generated package violates the contract."""


def _is_text_file(path: Path) -> bool:
    return path.suffix.casefold() in TEXT_EXTENSIONS or path.name in {
        "SKILL.md",
        "LICENSE",
        "README",
    }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise BuildError(f"expected UTF-8 text file: {path}") from error


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def discover_skill_dirs(education_root: Path) -> list[Path]:
    if not education_root.is_dir():
        raise BuildError(f"education root does not exist: {education_root}")
    skill_dirs = [
        child
        for child in sorted(education_root.iterdir())
        if child.is_dir()
        and child.name.startswith(PROMOTED_SKILL_PREFIX)
        and (child / "SKILL.md").is_file()
    ]
    if not skill_dirs:
        raise BuildError(f"no {PROMOTED_SKILL_PREFIX}* skill directories found in {education_root}")
    names = [path.name for path in skill_dirs]
    if len(names) != len(set(names)):
        raise BuildError("duplicate Education skill directory names")
    return skill_dirs


def _runtime_ignore(_directory: str, names: Sequence[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in RUNTIME_EXCLUDED_DIRS or name in RUNTIME_EXCLUDED_FILES:
            ignored.add(name)
        elif name.endswith((".pyc", ".pyo")):
            ignored.add(name)
    return ignored


def copy_skill_runtime(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination, ignore=_runtime_ignore)


def copy_shared_runtime(shared_source: Path, skill_destination: Path) -> Path:
    if not shared_source.is_dir():
        raise BuildError(f"shared source does not exist: {shared_source}")
    destination = skill_destination / "_shared"
    if destination.exists():
        shutil.rmtree(destination)

    def ignore_shared(_directory: str, names: Sequence[str]) -> set[str]:
        ignored = _runtime_ignore(_directory, names)
        ignored.update(name for name in names if name in {"fixtures", "scripts"})
        return ignored

    shutil.copytree(shared_source, destination, ignore=ignore_shared)
    init_path = destination / "__init__.py"
    if not init_path.exists():
        _write_text(
            init_path,
            '"""Vendored Zamery Education contracts for this standalone skill."""\n',
        )
    return destination


def _local_bootstrap() -> str:
    return (
        "_SKILL_ROOT = Path(__file__).resolve().parents[1]\n"
        "if str(_SKILL_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(_SKILL_ROOT))\n"
    )


def rewrite_python_runtime(content: str) -> str:
    """Replace monorepo imports/bootstrap with a skill-local vendored import."""
    has_monorepo_import = bool(MONOREPO_IMPORT_RE.search(content))
    content = MONOREPO_IMPORT_RE.sub(r"from _shared\g<suffix> import ", content)
    content = REPO_ROOT_ASSIGN_RE.sub("", content)
    content = REPO_ROOT_INSERT_RE.sub("", content)
    if has_monorepo_import and "_SKILL_ROOT = Path(__file__).resolve().parents[1]" not in content:
        import_match = re.search(r"(?m)^from _shared(?:\.[A-Za-z_][A-Za-z0-9_]*)? import ", content)
        if import_match is None:
            raise BuildError("failed to locate rewritten _shared import")
        content = content[: import_match.start()] + _local_bootstrap() + "\n" + content[import_match.start() :]
    return content


def rewrite_standalone_paths(skill_dir: Path) -> None:
    shared_root = skill_dir / "_shared"
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or not _is_text_file(path):
            continue
        content = _read_text(path)
        relative_shared = os.path.relpath(shared_root, path.parent).replace(os.sep, "/")

        def rewrite_shared_path(match: re.Match[str]) -> str:
            suffix = match.group("path").split("_shared/", maxsplit=1)[1]
            return f"{relative_shared}/{suffix}"

        rewritten = SHARED_PATH_RE.sub(rewrite_shared_path, content)
        if path.suffix.casefold() == ".py":
            rewritten = rewrite_python_runtime(rewritten)
        rewritten = rewritten.replace("skills.education._shared", "_shared")
        if rewritten != content:
            _write_text(path, rewritten)


def _frontmatter_name(skill_file: Path) -> str:
    content = _read_text(skill_file)
    if not content.startswith("---\n"):
        raise BuildError(f"SKILL.md missing YAML frontmatter: {skill_file}")
    match = FRONTMATTER_NAME_RE.search(content)
    if match is None:
        raise BuildError(f"SKILL.md missing frontmatter name: {skill_file}")
    return match.group("name")


def _iter_runtime_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise BuildError(f"standalone package contains symlink: {path}")
        if path.is_file():
            yield path


def _path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def certify_standalone_skill(skill_dir: Path) -> dict[str, object]:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise BuildError(f"missing SKILL.md in {skill_dir}")
    declared_name = _frontmatter_name(skill_file)
    if declared_name != skill_dir.name:
        raise BuildError(
            f"frontmatter name {declared_name!r} does not match directory {skill_dir.name!r}"
        )
    shared_dir = skill_dir / "_shared"
    if not (shared_dir / "__init__.py").is_file():
        raise BuildError(f"missing vendored _shared package in {skill_dir}")
    if not (shared_dir / "references").is_dir():
        raise BuildError(f"missing vendored shared references in {skill_dir}")

    text_file_count = 0
    total_file_count = 0
    for path in _iter_runtime_files(skill_dir):
        total_file_count += 1
        if not _path_is_within(path, skill_dir):
            raise BuildError(f"package file escapes skill root: {path}")
        if not _is_text_file(path):
            continue
        text_file_count += 1
        content = _read_text(path)
        for pattern, label in FORBIDDEN_STANDALONE_PATTERNS.items():
            if pattern in content:
                relative = path.relative_to(skill_dir)
                raise BuildError(f"{skill_dir.name}/{relative}: {label}: {pattern}")
        for match in SHARED_PATH_RE.finditer(content):
            token = match.group("path")
            target = (path.parent / token).resolve()
            if not _path_is_within(target, skill_dir):
                relative = path.relative_to(skill_dir)
                raise BuildError(
                    f"{skill_dir.name}/{relative}: parent-directory shared dependency escapes skill root: {token}"
                )
            if not target.exists():
                relative = path.relative_to(skill_dir)
                raise BuildError(
                    f"{skill_dir.name}/{relative}: shared dependency target is missing: {token}"
                )

    with tempfile.TemporaryDirectory(prefix=f"compile-{skill_dir.name}-") as temp_dir:
        compile_root = Path(temp_dir)
        for python_file in sorted(skill_dir.rglob("*.py")):
            relative = python_file.relative_to(skill_dir)
            pyc_path = compile_root / relative.with_suffix(".pyc")
            pyc_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                py_compile.compile(
                    str(python_file),
                    cfile=str(pyc_path),
                    dfile=relative.as_posix(),
                    doraise=True,
                )
            except py_compile.PyCompileError as error:
                raise BuildError(
                    f"Python compilation failed for {skill_dir.name}/{relative}: {error.msg}"
                ) from error

    return {
        "skill_name": skill_dir.name,
        "declared_name": declared_name,
        "file_count": total_file_count,
        "text_file_count": text_file_count,
        "standalone": True,
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _zip_directory(source_dir: Path, zip_path: Path, include_root: bool) -> None:
    """Create a deterministic ZIP with stable ordering, timestamps, and modes."""
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in _iter_runtime_files(source_dir):
            relative = path.relative_to(source_dir)
            arcname = (
                PurePosixPath(source_dir.name, *relative.parts)
                if include_root
                else PurePosixPath(*relative.parts)
            )
            info = zipfile.ZipInfo(arcname.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = path.stat().st_mode & 0o777
            info.external_attr = mode << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(zip_path, "r") as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise BuildError(f"ZIP CRC verification failed: {zip_path}: {bad_member}")


def _git_revision(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def build_suite(
    repo_root: Path,
    output_root: Path,
    *,
    expected_skill_count: int | None = 16,
) -> list[BuildResult]:
    education_root = repo_root / "skills" / "education"
    shared_source = education_root / "_shared"
    skill_sources = discover_skill_dirs(education_root)
    if expected_skill_count is not None and len(skill_sources) != expected_skill_count:
        raise BuildError(
            f"expected {expected_skill_count} Education skills, discovered {len(skill_sources)}"
        )

    packages_root = output_root / "skills"
    zips_root = output_root / "zips"
    if output_root.exists():
        shutil.rmtree(output_root)
    packages_root.mkdir(parents=True)
    zips_root.mkdir(parents=True)

    revision = _git_revision(repo_root)
    results: list[BuildResult] = []
    package_manifests: list[dict[str, object]] = []
    for source in skill_sources:
        destination = packages_root / source.name
        copy_skill_runtime(source, destination)
        copy_shared_runtime(shared_source, destination)
        rewrite_standalone_paths(destination)
        certification = certify_standalone_skill(destination)
        build_manifest = {
            "schema_version": "zamery-standalone-skill.v1",
            "skill_name": source.name,
            "source_revision": revision,
            "source_path": source.relative_to(repo_root).as_posix(),
            "vendored_shared_path": "_shared",
            "excluded_dev_directories": sorted(RUNTIME_EXCLUDED_DIRS),
            "certification": certification,
        }
        _write_text(
            destination / "BUILD-MANIFEST.json",
            json.dumps(build_manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        )
        # Re-certify after writing the build manifest.
        certification = certify_standalone_skill(destination)
        build_manifest["certification"] = certification
        _write_text(
            destination / "BUILD-MANIFEST.json",
            json.dumps(build_manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        )

        zip_path = zips_root / f"{source.name}.zip"
        _zip_directory(destination, zip_path, include_root=True)
        sha256 = _sha256(zip_path)
        result = BuildResult(
            skill_name=source.name,
            package_dir=destination,
            zip_path=zip_path,
            file_count=int(certification["file_count"]),
            sha256=sha256,
        )
        results.append(result)
        package_manifests.append(
            {
                "skill_name": result.skill_name,
                "file_count": result.file_count,
                "zip": result.zip_path.relative_to(output_root).as_posix(),
                "sha256": result.sha256,
            }
        )

    suite_manifest = {
        "schema_version": "zamery-standalone-suite.v1",
        "source_revision": revision,
        "skill_count": len(results),
        "skills": package_manifests,
    }
    _write_text(
        output_root / "SUITE-MANIFEST.json",
        json.dumps(suite_manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
    )
    suite_zip = output_root / "zamery-education-standalone.zip"
    _zip_directory(packages_root, suite_zip, include_root=False)
    suite_manifest["suite_zip"] = suite_zip.name
    suite_manifest["suite_zip_sha256"] = _sha256(suite_zip)
    _write_text(
        output_root / "SUITE-MANIFEST.json",
        json.dumps(suite_manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
    )
    return results


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: parent of scripts/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="output directory (default: <repo>/dist/education-standalone)",
    )
    parser.add_argument(
        "--expected-skill-count",
        type=int,
        default=16,
        help="fail unless this many Education skills are discovered; use 0 to disable",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    output_root = (
        args.output.resolve()
        if args.output is not None
        else repo_root / "dist" / "education-standalone"
    )
    expected = args.expected_skill_count or None
    try:
        results = build_suite(repo_root, output_root, expected_skill_count=expected)
    except BuildError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"built and certified {len(results)} standalone Education skills")
    for result in results:
        print(f"- {result.skill_name}: {result.file_count} files, {result.sha256[:12]}")
    print(f"suite: {output_root / 'zamery-education-standalone.zip'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
