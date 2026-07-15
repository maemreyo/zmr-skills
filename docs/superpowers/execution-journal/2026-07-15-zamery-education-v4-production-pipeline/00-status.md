# Zamery Education V4 implementation status

- Source plan: `docs/superpowers/plans/2026-07-15-zamery-education-v4-production-pipeline-design`
- Target base: `maemreyo/zmr-skills@zmr-dev`
- Verified base commit: `da1d6a7c602fa9e152b587c8698964b4c38d8dc2`
- Delivery form: isolated repository overlay with checksum manifest and backup-aware installer
- Cutover state: remains `v3`; no production tag, push, canary acceptance, or hard cutover was performed

## Scope

Tasks 1–37 are implemented as code, tests, schemas, policies, fixtures, workflows, and documentation. Task 38 operational tooling is implemented, but its irreversible/external actions are deliberately left for an authorized operator after release evidence and teacher acceptance exist.

## Verification boundaries

The sandbox can run Python 3.13, Node 22, LibreOffice, pytest, protocol parity, DOCX/PPTX/PDF reopen/rerender, archive security, determinism replay, and SQLite rebuild. It cannot download the requested Python 3.12 dev environment because outbound DNS is blocked; therefore Ruff, mypy, Hypothesis property runs, wheel build in a clean 3.12 environment, and a real pinned container build must be rerun after apply. Production container verification is fail-closed until `EDUCATION_V4_PYTHON_BASE_IMAGE` is configured to an immutable `@sha256:` reference.
