# Delivery Formats

| Format | Owning workflow | File checks |
|---|---|---|
| DOCX | Documents | render every page; check headings, breaks, tables, and answer separation |
| PDF | PDF | render every page; check fonts, links, page boxes, and answer separation |
| PPTX | Presentations | render every slide; check clipping, notes, interactions, and fallbacks |
| offline HTML | direct artifact creation | no network dependency, keyboard use, print mode, embedded assets |
| TSV/CSV | Spreadsheets | encoding, delimiter, header order, row counts, formula-free export unless requested |
| JSONL/SQLite | item-bank workflow | JSON records/counts; SQLite integrity/tables/versions |
| IMS QTI | assessment composer | CRC, XML, manifest, item references, target-LMS smoke test |
| H5P | video-learning workflow | CRC, package/content JSON, dependencies, target-platform smoke test |

Deferred and unsupported until a dedicated exporter and validator exist: GIFT, Anki `.apkg`, generated audio, and generated video. State the exact limitation and offer only supported alternatives; do not rename or approximate a file as if it were certified.

Name deliverables with the pattern `zamery-{brief_slug}-{artifact_type}-v{version}-{audience}.{extension}` using lowercase ASCII slugs and `student` or `teacher` audience. A combined pack may use audience `mixed` only when its internal student and teacher sections remain structurally separate.
## V3 structured exports

JSONL is the portable canonical item projection; reopen every non-empty line as one JSON object and verify IDs/counts. SQLite is the operational bank; run `PRAGMA integrity_check`, verify required tables, versions, and counts. QTI packages require ZIP CRC, XML parsing, manifest/test files, declared item resources, and an import smoke test where a target LMS is available. H5P packages require ZIP CRC, mandatory `h5p.json`, `content/content.json`, declared dependencies, interaction counts, and a target-platform import test. Host-resolved H5P exports do not bundle libraries and must say so.

QTI and H5P are delivery formats, never the canonical authoring database.
