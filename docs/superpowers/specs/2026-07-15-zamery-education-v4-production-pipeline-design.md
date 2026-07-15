# Zamery Education V4 Production Pipeline Design

> **Status:** Approved design, ready for implementation planning  
> **Date:** 15 July 2026  
> **Target branch:** `zmr-dev`  
> **Release strategy:** Breaking V4, built side-by-side with frozen V3, followed by hard cutover  
> **Scope:** Framework-first, full production pipeline

## 1. Executive summary

Zamery Education V4 replaces the current prose-led, manifest-trusting pipeline with a graph-native production system whose authority is carried by immutable typed records, content hashes, explicit approvals, independently produced evidence receipts, and deterministic gate decisions.

The V4 runtime uses a shared governance kernel plus isolated capability modules. The kernel owns lifecycle state, the artifact graph, approvals, deterministic DAG execution, cache and invalidation, evidence, quality-gate policies, canonical storage, migrations, and publication state. Pedagogy, content authoring, document composition, rendering, inspection, and publishing remain independent capabilities connected through a language-neutral JSON subprocess protocol.

DOCX, PDF, PPTX, HTML, archives, and structured exports are projections rather than sources of truth. Every published file must be traceable to approved planning and content records, independently inspected, rendered where applicable, and included in a delivery bundle by exact graph membership rather than folder globbing.

The first production acceptance fixture is the audited *Mindset for IELTS Foundation*, Unit 1 Lesson 1 pack. V4 must detect every confirmed failure from that audit and produce a replacement pack that passes all seven quality gates.

## 2. Problem statement

The current Education suite contains useful contracts, specialist boundaries, templates, and quality-gate language, but enforcement is incomplete and fragmented.

Confirmed failure modes include:

1. Routing can classify a coursebook lesson-design request as `ielts_practice` merely because the request contains the word `IELTS`.
2. Validators primarily confirm record shape and declared fields rather than instructional completeness or cross-artifact coherence.
3. Source lineage is not preserved across source, objective, activity, item, artifact, answer authority, and scoring decision.
4. Thresholds such as `5/7` or `8/10` may appear in teacher-facing files without deterministic item membership.
5. Generated transfer content can coexist with source activity without a governed distinction between core work and supplement.
6. A deck manifest can satisfy teacher-note mapping while all note content is empty.
7. Render QA can fail at runtime while downstream manifests still contain declared pass booleans.
8. Pack validation can trust flags such as `reopened`, `reextracted`, or `rerendered` instead of receipts produced by those operations.
9. Generators can effectively attest to the validity of their own outputs.
10. No shared execution state guarantees that student materials, teacher guides, answer keys, presentations, and publication bundles were derived from the same approved inputs.

These are execution-architecture and governance failures. Adding more prose rules or more required manifest fields would not reliably prevent recurrence.

## 3. Goals

V4 must:

1. Make every material teaching decision, source dependency, objective, item, answer, artifact, binary, approval, receipt, gate decision, and published file traceable by content hash.
2. Replace mutable approval flags with immutable approvals tied to exact record or subgraph hashes.
3. Replace single-intent routing with a governed multi-stage workflow plan.
4. Execute work through a deterministic DAG with precise cache keys and downstream invalidation.
5. Isolate capabilities in sandboxed subprocesses with declared inputs, outputs, runtimes, side effects, permissions, and failure codes.
6. Treat canonical JSON records as authority and SQLite as a disposable query index.
7. Require independent evidence producers for binary reopening, rendering, accessibility, safety, notes, archive integrity, and other quality claims.
8. Make all seven quality gates explainable and evidence-driven.
9. Support selective repair and deterministic resume from the failed dependency boundary.
10. Re-extract, reopen, rerender, and revalidate a candidate bundle before publication.
11. Provide production-grade testing, migration receipts, golden workflows, CI, and hard-cutover criteria.
12. Keep V4 language-neutral at capability boundaries while using a typed Python kernel.

## 4. Non-goals

V4 does not include:

1. A teacher dashboard or artifact-management web application.
2. Runtime compatibility with V3 schemas or validators.
3. Automatic teacher approval by a model.
4. A universal pedagogical-quality algorithm that replaces professional review.
5. Byte-for-byte determinism for third-party office binaries when external tooling embeds unavoidable volatile metadata; semantic determinism remains mandatory.
6. Reproduction or redistribution rights for copyrighted source materials beyond the authority represented in source and copyright records.
7. A model scratchpad, hidden reasoning archive, or prompt-history database in canonical domain records.

## 5. Approved architectural decisions

- **Release:** breaking V4.
- **Scope:** full production pipeline, not governance-only.
- **Architecture:** shared kernel plus capability modules and side-effect adapters.
- **Authority model:** typed artifact graph with immutable records.
- **Storage:** content-addressed canonical JSON plus a rebuildable SQLite index.
- **Execution:** deterministic DAG executor.
- **Capability isolation:** typed JSON protocol over sandboxed subprocesses.
- **Core stack:** Python 3.12, Pydantic v2, generated JSON Schema, language-neutral adapters.
- **Approval:** immutable approval records tied to exact hashes.
- **Quality:** evidence-driven gate engine with independent receipts and human review records.
- **Migration:** V4 side-by-side with frozen V3, then hard cutover without runtime compatibility adapters.

## 6. System architecture

```text
Teacher / CLI / agent entry points
                 |
                 v
        Application orchestrator
     request resolution · run planning
                 |
                 v
+---------------- Shared kernel ----------------+
| Record registry                               |
| Artifact graph                                |
| Approval authority                            |
| Deterministic DAG executor                    |
| Evidence and gate engine                      |
| Canonical store and rebuildable index         |
| Migration registry                            |
+-------------------+----------------------------+
                    | typed capability protocol
        +-----------+---------------+
        v           v               v
 Pedagogy       Composition      Verification
 capabilities   capabilities     capabilities
        |           |               |
        +-----------+---------------+
                    v
           Sandboxed adapters
 DOCX · PDF · PPTX · browser · LibreOffice · ZIP
```

### 6.1 Shared kernel responsibilities

The kernel owns only cross-cutting governance and execution behavior:

- record models and schema registry;
- canonical serialization and hashing;
- graph construction, traversal, and invariants;
- approval applicability and revocation;
- execution-plan construction;
- DAG scheduling, caching, invalidation, and resume;
- capability protocol validation;
- evidence receipt registration;
- gate policy evaluation;
- canonical store and SQLite index rebuild;
- migration registry;
- publication-state transitions.

The kernel does not author lesson content, compose slides, generate office files, judge pedagogy, or render artifacts.

### 6.2 Application layer

```text
src/zamery_education_v4/application/
├── request_resolution/
├── run_planning/
├── impact_analysis/
├── repair_planning/
├── review_workflows/
└── publication/
```

The application layer converts a user request and current graph state into governed commands for the kernel without embedding adapter details.

### 6.3 Capability modules

```text
capabilities/
├── pedagogy/
│   ├── resolve_teaching_request/
│   ├── build_teaching_brief/
│   ├── design_learning_blueprint/
│   └── review_pedagogy_packet/
├── content/
│   ├── author_practice_content/
│   ├── author_homework_mission/
│   └── establish_answer_authority/
├── composition/
│   ├── compose_student_material/
│   ├── compose_teacher_guide/
│   ├── compose_answer_key/
│   └── compose_presentation/
├── verification/
│   ├── inspect_source_lineage/
│   ├── inspect_accessibility/
│   ├── inspect_binary/
│   ├── inspect_render/
│   └── inspect_archive/
└── publishing/
    └── assemble_delivery_bundle/
```

A capability may consume only declared record types and mounted input files and may emit only declared output record types and file descriptors. It cannot mutate the graph, grant approval, declare a quality-gate pass, or read arbitrary repository files.

### 6.4 Adapter boundary

```text
adapters/
├── docx/
├── pdf/
├── pptx/
├── browser/
├── libreoffice/
├── filesystem/
├── archive/
└── model_runtime/
```

Generation, reopening, rendering, inspection, and publication are separate graph nodes. A generator cannot issue the receipt that validates its own output.

### 6.5 V3 and V4 boundary

During development:

```text
skills/education/          # V3 frozen
skills/education_v4/       # V4 agent-facing entry surfaces
src/zamery_education_v4/   # V4 runtime
capabilities/              # V4 capability implementations
adapters/                  # V4 side-effect integrations
schemas/v4/
policies/v4/
migrations/v4/
goldens/v4/
tests/v4/
```

V4 does not import V3 runtime, validators, schema models, or compatibility shims. Golden requests may run through both pipelines for comparison only.

## 7. Canonical data model

### 7.1 Record requirements

Every canonical record must:

- have `record_type` and semantic `schema_version`;
- validate through a registered Pydantic model;
- serialize through a canonical JSON encoder;
- be immutable after commit;
- have a stable logical identifier and a calculated `content_hash`;
- declare typed relationships to other record hashes or IDs;
- exclude mutable build status and unverified quality booleans;
- exclude temporary machine paths, process identifiers, hostnames, secrets, model scratchpads, and irrelevant timestamps.

### 7.2 Record families

#### Context and authority

- `TeachingRequest`
- `SourceRecord`
- `CopyrightUseRecord`
- `TeachingBrief`
- `LearnerContextSnapshot`
- `AuthorityRecord`
- `ApprovalRecord`

A `SourceRecord` carries source identity, edition or version, binary hash, access scope, authority class, and permitted use. An `AuthorityRecord` distinguishes direct source, authorized excerpt, teacher-approved adaptation, official answer authority, teacher-authored answer authority, original supplement, and unsupported inference.

#### Planning

- `LearningSequenceMap`
- `LearningBlueprint`
- `ObjectiveRecord`
- `SuccessEvidenceRecord`
- `MisconceptionRecord`
- `MethodologyRecord`
- `AssessmentDecisionRule`
- `AccommodationDecisionRecord`

An `AssessmentDecisionRule` contains exact item membership. Its denominator is derived from unique membership rather than stored as an unrelated display number.

#### Content

- `ContentUnit`
- `PassageRecord`
- `ItemRecord`
- `PromptRecord`
- `AnswerRecord`
- `RubricRecord`
- `FeedbackModel`
- `HomeworkMission`

A `ContentUnit` declares a role such as `core_source_activity`, `teacher_approved_adaptation`, `original_supplement`, `generated_near_transfer`, `retrieval`, or `assessment`. A generated transfer activity cannot replace a required core activity without material teacher approval.

#### Artifact specifications

- `StudentWorksheetSpec`
- `StudentWorkbookSpec`
- `TeacherGuideSpec`
- `AnswerKeySpec`
- `ObservationFormSpec`
- `PresentationSpec`
- `HomeworkSpec`
- `DeliveryBundleSpec`

Specifications contain content membership, audience, objective lineage, answer-visibility policy, response-space requirements, accessibility requirements, source references, and format-independent layout intent.

#### Generated and rendered artifacts

- `GeneratedArtifact`
- `RenderedArtifact`
- `PublishedBundleRecord`

A generated artifact records its specification hash, format, binary hash, generator capability and version, runtime digest, and bundle-relative output path. A rendered artifact records the exact input binary hash, renderer identity, runtime digest, page or slide output hashes, and semantic fingerprint.

#### Evidence and decisions

- `ExecutionPlan`
- `ExecutionReceipt`
- `MigrationReceipt`
- `SourceLineageReceipt`
- `ObjectiveCoverageReceipt`
- `AnswerAuthorityReceipt`
- `DecisionRuleReceipt`
- `AnswerSeparationReceipt`
- `BinaryInspectionReceipt`
- `RenderInspectionReceipt`
- `AccessibilityReceipt`
- `ArchiveIntegrityReceipt`
- `ReviewRecord`
- `GateDecision`
- `RepairPlan`

### 7.3 Typed graph edges

Supported edge types include:

- `DERIVED_FROM`
- `REFERENCES`
- `IMPLEMENTS_OBJECTIVE`
- `USES_AUTHORITY`
- `USES_DURATION`
- `PROJECTS_TO`
- `GENERATED_FROM`
- `RENDERED_FROM`
- `VERIFIED_BY`
- `APPROVED_BY`
- `SUPERSEDES`
- `REVOKES`
- `INVALIDATES`
- `PACKAGES`

The graph model defines permitted source and target record families for every edge type.

### 7.4 Mandatory graph invariants

The kernel rejects a graph when:

1. A prohibited dependency cycle exists.
2. A record references a missing or superseded required dependency.
3. An artifact specification references an unknown content unit or objective.
4. A student artifact includes teacher-only answers, rubrics, rationales, or notes.
5. A scored item lacks answer authority.
6. A decision rule's denominator differs from its unique item-membership count.
7. A generated artifact lacks an exact specification hash.
8. A render or inspection receipt targets a different binary hash from the artifact under review.
9. A gate decision uses receipts from a different subject version.
10. An approval targets a hash that is missing, revoked, or outside its scope.
11. A delivery bundle contains an artifact without required gate decisions.
12. A generated transfer replaces a core source activity without material approval.
13. A bundle contains an untracked file or omits a declared file.
14. An answer key omits an item that a teacher decision rule or active lesson stage requires.
15. A teacher guide, deck, and answer surface refer to incompatible decision-rule versions.

## 8. Storage model

### 8.1 Canonical store

```text
.zamery/
├── records/<record_type>/<sha256>.json
├── blobs/<sha256>.<extension>
├── graphs/<pack-id>.graph.json
├── approvals/<sha256>.json
├── runs/<execution-id>/
└── index/graph.sqlite
```

Canonical serialization uses sorted object keys, normalized Unicode, explicit number handling, no insignificant whitespace, and schema-defined ordering for semantically unordered collections.

### 8.2 SQLite index

SQLite is a disposable index for record lookup, dependency traversal, run queries, and cache metadata. It is never the authority for domain content or gate state.

CI deletes the database, rebuilds it from canonical records, and confirms identical node count, edge count, graph hash, approval resolution, gate-decision resolution, and cache identities.

## 9. Approval model

Material authority is represented by immutable `ApprovalRecord` instances.

Each approval records:

- exact approved record hashes or subgraph hash;
- approval scope, such as brief, source authority, objectives, pedagogy, content, artifact specification, repair, or publication;
- approver identity or role;
- approval timestamp;
- accepted assumptions and limitations;
- optional signature metadata;
- supersedes and revokes relationships.

Executor nodes that require teacher authority cannot run without an applicable, current approval for the exact input hashes. Any material record change creates a new hash and makes the prior approval inapplicable without mutating the prior record.

## 10. Request resolution and workflow planning

The V4 router returns a `WorkflowPlan`, not a single intent string.

Routing precedence is:

1. requested deliverable and lifecycle goal;
2. current workflow stage;
3. source type and source sensitivity;
4. graded versus ungraded status;
5. domain profile, including IELTS task-family constraints;
6. quantity and reuse expectations;
7. requested output formats.

A request to create a complete lesson pack for *Mindset for IELTS Foundation* resolves to a workflow containing source authority, brief, blueprint, content authoring, material composition, presentation composition, verification, and publication. The IELTS profile constrains relevant content but does not replace lesson design as the workflow goal.

## 11. Deterministic DAG execution

### 11.1 Planning

Before execution, the kernel creates an immutable `ExecutionPlan` containing:

- input graph hash;
- requested target IDs;
- required capability nodes;
- exact capability versions and runtime digests;
- input record hashes;
- expected output types;
- dependency edges;
- cache keys;
- approval prerequisites;
- policy versions relevant to cache and gate behavior.

A run may proceed only while the graph and required approvals still match the plan.

### 11.2 Cache identity

The cache key is calculated from:

```text
capability ID
+ capability version
+ runtime digest
+ protocol version
+ sorted input record hashes
+ normalized configuration
+ relevant policy versions
```

It excludes machine paths, hostname, run timestamp, invocation ID, and temporary output directory.

A cache entry is usable only when output records and blobs exist, hashes validate, schemas remain supported, capability runtime is not revoked, approval scope remains valid, and no policy requires fresh evidence.

### 11.3 Selective invalidation

Typed dependency edges determine invalidation. A changed teaching duration may invalidate the blueprint, teacher guide, slide timing notes, and rendered artifacts while preserving unrelated source, vocabulary, and answer records.

Impact analysis produces an explicit report of changed records, invalidated nodes, preserved nodes, and dependency reasons. Material changes require approval at the affected scope only.

### 11.4 Resume and failure boundaries

A failed node does not erase valid prior outputs. Resume begins from the failed node or earliest newly invalidated dependency. The executor never edits the previous receipt or gate decision; it creates new records for each attempt.

## 12. Capability protocol and sandbox

### 12.1 Manifest

Each capability declares:

- capability ID and semantic version;
- protocol version;
- input and output record types;
- deterministic status;
- side-effect class;
- timeout and resource limits;
- runtime language, version, digest, and lockfile hash;
- filesystem and network permissions;
- cache policy;
- supported platforms;
- failure codes;
- supported migration versions.

### 12.2 Invocation protocol

The kernel invokes a capability using one JSON object on stdin. Stdout contains exactly one protocol result object. Logs go to stderr.

Inputs are read-only mounted files or canonical record paths. Outputs must be created in a fresh writable output mount. The result lists every output record and produced-file descriptor with a declared hash.

The kernel independently parses, validates, canonicalizes, rehashes, checks output-type permission, checks references, and enforces cross-record invariants before committing any result.

### 12.3 Capability classes

- **Pure transformations:** deterministic record-to-record operations with no network or binary side effects.
- **Model-assisted authoring:** record model/provider identity, configuration, prompt-template hash, and response hash in execution receipts; require schema validation and human review where policy demands it.
- **Side-effect adapters:** generate or transform binaries from approved specifications.
- **Evidence producers:** inspect records or binaries and emit immutable receipts and findings.
- **Human review workflows:** prepare review packets and accept structured reviewer decisions as `ReviewRecord` instances.

### 12.4 Sandbox defaults

- network denied;
- read-only input mount;
- empty output mount;
- no repository-wide view;
- no user home or environment secrets;
- mandatory timeout;
- stdout, file-count, and output-size limits;
- no symlinks;
- path-containment enforcement;
- zip-slip protection;
- executable and runtime digest verification.

A research capability declares an allowlist and creates research evidence containing source URL, access time, authority class, and supported claims.

## 13. Failure model

Failure categories:

- `INPUT`
- `AUTHORITY`
- `POLICY`
- `CAPABILITY`
- `TOOL`
- `RESOURCE`
- `OUTPUT`
- `HUMAN_REVIEW`

Representative failure codes:

- `INPUT_SCHEMA_INVALID`
- `INPUT_HASH_MISMATCH`
- `APPROVAL_MISSING`
- `APPROVAL_STALE`
- `SOURCE_AUTHORITY_CONFLICT`
- `CAPABILITY_TIMEOUT`
- `CAPABILITY_PROTOCOL_INVALID`
- `TOOL_NOT_INSTALLED`
- `BINARY_REOPEN_FAILED`
- `OUTPUT_SCHEMA_INVALID`
- `OUTPUT_HASH_MISMATCH`
- `GATE_HARD_BLOCK`
- `HUMAN_REVIEW_REQUIRED`

The executor retries only failures declared retryable by policy. Authority conflicts, stale approvals, answer leakage, unsupported source use, and deterministic output-schema violations are not retried for unchanged inputs.

## 14. Evidence-driven quality gates

V4 retains seven ordered gates:

1. Brief
2. Pedagogy
3. Content
4. Safety
5. Accessibility
6. Presentation
7. Pack

A gate policy consumes canonical record hashes, independent evidence receipts, applicable approvals, and human `ReviewRecord` instances. It cannot trust self-declared booleans. A later gate cannot pass while an earlier gate has an unresolved hard block.

Every `GateDecision` records:

- gate and policy version;
- exact subject graph hash;
- receipt and review hashes consumed;
- pass, repair-required, or fail decision;
- hard-block status;
- findings and affected IDs;
- deterministic or human-reviewed basis;
- expiry and invalidation conditions.

### 14.1 Brief gate

Required evidence includes schema, source identity, learner-context boundary, constraint coverage, and approval coverage.

Hard blocks include unresolved material fields, unknown source version for source-sensitive work, CEFR inferred without authority, protected learner data in downstream context, and missing or stale approval.

### 14.2 Pedagogy gate

Automated evidence checks objective observability, phase alignment, timing totals, scaffold progression, distinct guided and independent memberships, assessment evidence, transfer role, and preservation of core source activity.

Production requires a teacher `ReviewRecord` using a versioned rubric covering learner fit, objective alignment, cognitive progression, misconception handling, assessment validity, workload, transfer quality, and delivery fit.

### 14.3 Content gate

Required inspectors cover source lineage, objective coverage, answer authority, decision rules, and cross-artifact consistency.

Hard blocks include:

- missing or contradictory source lineage;
- missing or stale answer authority;
- decision-rule denominator mismatch;
- core source activity replaced by transfer;
- unknown objective lineage;
- incompatible item membership across surfaces;
- visible content error;
- teacher guide, deck, and answer key using inconsistent versions.

### 14.4 Safety gate

Record-level checks cover PII, protected learner data, teacher-only leakage, AI-use policy, media-task privacy, consent, alternative submission routes, copyright-use classification, and ownership verification.

Binary checks cover comments, revisions, hidden slides, notes, embedded objects, metadata, PDF annotations, image EXIF, macros, and external relationships.

Media homework for minors must offer face-free and private-space-free options, prohibit bystanders without consent, require a private submission channel, define retention and deletion policy, and include a teacher nonce or live follow-up where ownership verification is claimed.

### 14.5 Accessibility gate

Evidence spans:

- DOCX semantic headings, language, title, table headers, reading order, and alt text;
- PPTX semantic titles, reading order, notes, alt text, and print fallback;
- PDF tags, language, title, reading order, table structure, selectable text, and raster-only detection;
- contrast, grayscale, minimum type size, response space, projection legibility, and non-color-dependent meaning;
- construct-preserving accommodation decisions.

An accommodation that changes the measured construct requires an explicit `AccommodationDecisionRecord` and approval.

### 14.6 Presentation gate

Document and slide checks cover clipping, overlap, orphan rows, sparse pages, response space, prompt/response geometry, print margins, duplex behavior, shape bounds, projected font floors, notes content, reveal behavior, hidden content, metadata, and print fallbacks.

Page-density policies are role-specific. Occupancy is supporting evidence rather than an automatic universal failure threshold. Semantic response areas distinguish purposeful writing space from accidental blank pages.

Production requires a visual review packet with page or slide thumbnails, geometry findings, type distribution, response-space map, contrast results, reading-order preview, and note coverage.

### 14.7 Pack gate

Bundle assembly uses exact `DeliveryBundleSpec` membership. Folder globbing is prohibited.

Verification chain:

1. assemble candidate directory;
2. verify every file hash against the graph;
3. reject missing and unknown files;
4. create archive;
5. verify CRC and archive security;
6. extract into a clean directory;
7. rehash extracted files;
8. reopen applicable formats;
9. rerender extracted classroom files;
10. compare semantic fingerprints and tolerated visual differences;
11. aggregate all seven gate decisions;
12. require publication approval;
13. create `PublishedBundleRecord`.

## 15. Independent verification rule

No capability may validate or grant a gate pass for its own generated output.

Example presentation chain:

```text
PresentationSpec
  -> PPTX generator
  -> PPTX binary inspector
  -> renderer
  -> render geometry inspector
  -> human visual review
  -> presentation gate policy
```

The nodes have distinct capability identities and receipts even when CI executes them on the same machine.

## 16. Repair workflow

```text
Finding
  -> materiality classification
  -> affected-subgraph calculation
  -> RepairPlan
  -> teacher approval when material
  -> selective invalidation
  -> rerun affected capabilities
  -> new receipts
  -> new GateDecision
```

Non-material repairs include metadata, typography, spacing, accessibility markup, and exporter defects when content meaning is unchanged. Material repairs include objectives, pedagogy, source substitution, scoring membership, grammar scope, or privacy-model changes.

Prior records and decisions remain immutable.

## 17. Production profiles

### Draft

- schema and graph invariants;
- student-answer leakage and baseline safety;
- basic binary generation;
- no publication.

### Review

- all automated evidence producers;
- visual and pedagogy review packets;
- structured findings and repair plans;
- no production publication.

### Production

- current approvals for exact hashes;
- required human reviews;
- full automated evidence;
- seven ordered gate passes;
- clean re-extraction, reopening, and rerender;
- publication approval;
- `PublishedBundleRecord`.

Every artifact and UI surface must show its profile clearly.

## 18. Migration

### 18.1 Principles

V4 migration is loss-explicit. It does not import V3 quality booleans as evidence and does not treat V3 binaries as canonical content.

Migration outcomes:

- `migrated`
- `requires_teacher_review`
- `requires_reauthoring`
- `rejected`

Automatically preserved data must have clear authority, such as explicit source identity, teacher-approved brief values, stable objective IDs, approved content, answer authority, and privacy-safe learner context.

Mutable approval flags, build status, inferred CEFR, unverified reopening flags, unsupported claims, and generated artifacts without lineage are discarded or routed to review with explicit reasons.

### 18.2 Migration receipt

Every migration creates a `MigrationReceipt` containing source hash, target hash, migration version, preserved fields, discarded fields, warnings, and required reviews. Silent field loss is prohibited.

### 18.3 Binary migration

Existing V3 PPTX or document files may be imported as visual or textual reference evidence. They cannot become V4 production artifacts without approved V4 content and specifications, regeneration or governed adoption, independent inspection, rendering, evidence, and gate decisions.

## 19. Testing strategy

### 19.1 Unit and schema tests

Every record type requires valid and invalid fixtures, forbidden mutable-field tests, canonicalization tests, round-trip serialization, and JSON Schema snapshots.

### 19.2 Property-based tests

Use Hypothesis to test:

- canonical ordering does not change hashes;
- semantic field changes do change hashes;
- forbidden machine-local fields cannot enter canonical records;
- dependency traversal is complete;
- decision-rule denominators equal unique membership;
- cache keys ignore hostname, timestamp, and temporary path;
- archive extraction remains contained;
- selective invalidation affects only reachable dependent nodes.

### 19.3 Graph tests

Cover cycle detection, missing nodes, invalid edge types, superseded dependencies, stale approvals, receipt-subject mismatches, evidence from wrong versions, untracked bundle files, deterministic plan ordering, and repair impact calculation.

### 19.4 Capability protocol conformance

A shared suite tests malformed stdout, mixed logs and JSON, declared-hash mismatch, output outside mount, unsupported record type, timeout, resource limit, symlink output, undeclared network access, oversized output, and partial output on failure.

### 19.5 Adapter integration tests

DOCX tests cover reopening, visible-text fingerprint, metadata, heading hierarchy, table headers, revisions, comments, macros, and external relationships.

PPTX tests cover reopening, slide count, semantic titles, shape and text bounds, non-empty mapped notes, hidden slides, external relationships, metadata, and print fallbacks.

PDF tests cover page count, extractable text, language, title, tags, reading order, clipping geometry, raster-only detection, annotations, and attachments.

Archive tests cover CRC, zip-slip, duplicate paths, case collisions, re-extraction, hash parity, reopening, and rerender from extracted files.

### 19.6 Pedagogical coherence testing

Machine checks cover objective coverage, scaffold reduction, distinct practice memberships, retrieval spacing, transfer role, source preservation, response-mode variation, evidence variation, workload, timing, and decision-rule membership.

Teacher review covers learner fit, authenticity, cognitive progression, distractor quality, reading discrimination, speaking ownership, diagnostic validity, source fidelity, and live teacher usability.

Golden assertions target structure and required findings rather than exact model-authored prose.

## 20. Golden acceptance workflows

V4 includes at least six production fixtures:

1. **Source-sensitive multi-artifact lesson:** Unit 1 Lesson 1, including source authority, core/transfer distinction, diagnostic, teacher and student surfaces, DOCX/PDF/PPTX, privacy-safe ownership homework, and publication.
2. **Standalone worksheet:** guided, independent, retrieval, response space, answer separation, and print output.
3. **Reusable 300-item bank:** routing, batching, deduplication, resumability, JSONL, SQLite, and CSV.
4. **100-item exam:** blueprint, forms, answer set, answer sheet, administration guide, QTI, and security.
5. **Video learning:** media authority, transcript provenance, timestamps, accessibility fallback, allowlisted research, and H5P.
6. **Learner evidence and reteaching:** protected-record boundaries, monitoring-before-reteaching, sufficiency, human judgment, and reassessment.

The Unit 1 fixture encodes all known audit failures as negative acceptance tests, including route misclassification, missing source lineage, unresolved denominators, empty notes, missing source answers, self-declared QA, broken render inspection, generic competing homework, and unsafe media requirements.

## 21. CI pipeline

```text
lint
  -> typecheck
  -> unit tests
  -> schema snapshots
  -> property tests
  -> capability protocol tests
  -> adapter integration tests
  -> golden draft runs
  -> golden production runs
  -> determinism replay
  -> clean SQLite rebuild
  -> clean bundle extraction and rerender
```

Required jobs:

- `v4-kernel`
- `v4-capability-contracts`
- `v4-docx-adapter`
- `v4-pptx-adapter`
- `v4-pdf-adapter`
- `v4-pack-security`
- `v4-golden-unit1`
- `v4-golden-bank`
- `v4-golden-assessment`
- `v4-determinism`
- `v4-migration`

Two clean runs must produce identical canonical record hashes, graph hash, execution-plan hash, cache identities, and semantic binary fingerprints. Deterministic archives normalize file order and permitted metadata.

## 22. Observability and explainability

Run logs are structured operational evidence, not domain authority.

Events:

- `RUN_PLANNED`
- `NODE_READY`
- `CACHE_HIT`
- `CAPABILITY_STARTED`
- `CAPABILITY_COMPLETED`
- `OUTPUT_REJECTED`
- `REVIEW_REQUIRED`
- `GATE_DECIDED`
- `REPAIR_PLANNED`
- `BUNDLE_PUBLISHED`

Events contain run ID, plan hash, node ID, capability identity, input and output hashes, duration, failure code, and correlation ID. Logs exclude full StudentCards, unnecessary student PII, secrets, hidden model reasoning, and raw document bodies unless explicitly needed and protected.

CLI commands:

```bash
zamery v4 run explain <run-id>
zamery v4 graph trace <artifact-id>
zamery v4 artifact provenance <hash>
zamery v4 impact --before <hash> --after <hash>
zamery v4 gate explain --decision <hash>
zamery v4 repair explain <repair-plan-id>
zamery v4 index rebuild
zamery v4 cache verify
```

`gate explain` states the policy, subject graph, evidence hashes, exact finding, affected IDs, required repair, and preserved nodes.

## 23. Technology stack

- Python 3.12
- Pydantic v2
- generated JSON Schema
- canonical JSON serializer owned by the kernel
- `sqlite3` or SQLAlchemy Core without a domain ORM
- Hypothesis
- `pytest`
- JSON stdin/stdout capability protocol
- Python and Node capability runtimes with independent lockfiles and runtime digests
- fit-for-purpose DOCX, PPTX, PDF, browser, and LibreOffice tooling behind adapters

V4 does not preserve Python 3.9 compatibility.

## 24. Repository layout

```text
src/zamery_education_v4/
├── application/
├── kernel/
│   ├── records/
│   ├── graph/
│   ├── approvals/
│   ├── execution/
│   ├── evidence/
│   ├── gates/
│   ├── storage/
│   └── migrations/
├── protocol/
├── policies/
└── cli/

skills/education_v4/
capabilities/
adapters/
schemas/v4/
policies/v4/
migrations/v4/
goldens/v4/
tests/v4/
docs/architecture/v4/
```

Skill folders remain agent-facing instructions and entry surfaces. Enforceable behavior belongs in runtime code, capability contracts, inspectors, and gate policies rather than solely in `SKILL.md` prose.

## 25. Side-by-side delivery and hard cutover

### 25.1 Development phase

- Freeze V3 except for critical safety fixes.
- Build V4 in separate packages and namespaces.
- Run shared golden requests through V3 and V4 for comparison.
- Do not introduce V3 schema compatibility into V4 runtime.
- Keep rollback at the entry-point or release-tag level.

### 25.2 Cutover criteria

Production entry points do not move to V4 until:

1. All record, graph, approval, and execution invariant tests pass.
2. Python and Node sample capabilities pass the common protocol suite.
3. Unit 1 Lesson 1 passes all seven gates as a production golden.
4. At least five additional golden workflows pass.
5. SQLite deletion and rebuild reproduce the same graph and decisions.
6. Two clean runs produce equivalent canonical and semantic outputs.
7. Re-extracted bundles reopen and rerender successfully.
8. Every known Unit 1 audit failure is detected by a negative test.
9. Comparison reports show no severe regression in supported V3 workflows.
10. Migration reports show no silent data loss.
11. Sandbox and archive security review passes.
12. A teacher confirms that command surfaces are usable during a real lesson.

### 25.3 Hard cutover wave

1. Tag final V3 state.
2. Freeze V3 writes.
3. Publish V4 migration and operator guides.
4. Switch the default Education entry point to V4.
5. Run production canary fixtures.
6. Monitor structured failures and gate behavior.
7. Remove V3 runtime in a separate change after canary acceptance.
8. Preserve the V3 tag and archived documentation.

Rollback during canary changes the entry point back to the V3 release. It does not load V3 records into V4.

## 26. Definition of done

V4 is complete only when the system can demonstrate:

> Starting from a teacher-approved request and governed source set, Zamery can create, inspect, repair selectively, and publish a multi-artifact teaching pack in which every objective, content unit, item, answer, artifact specification, binary, render, approval, evidence receipt, gate decision, and bundle file is traceable by content hash; no quality claim depends on a self-declared boolean; and the published bundle can be independently re-extracted, reopened, rerendered, and revalidated from the records and receipts delivered with it.

## 27. Requirements for the implementation plan

The implementation plan derived from this design must:

- use vertical slices that produce executable behavior early;
- start with kernel contracts and failing tests;
- keep each capability and adapter behind a narrow protocol boundary;
- create negative fixtures for every audited failure;
- avoid implementing a dashboard or unrelated platform features;
- make Unit 1 the first production tracer bullet without hard-coding the framework to that coursebook;
- specify exact files, interfaces, tests, commands, and verification evidence for every task;
- include migration, CI, documentation, and cutover work rather than stopping after core models.
