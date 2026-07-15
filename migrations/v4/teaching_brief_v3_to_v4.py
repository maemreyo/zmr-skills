from __future__ import annotations
from zamery_education_v4.kernel.migrations.runner import MigrationContext
from zamery_education_v4.kernel.records.migration import MigrationOutcome
from ._common import classify_and_migrate
SOURCE_SCHEMA = "teaching-brief.v3"
TARGET_SCHEMA = "teaching-brief.v4"
def migrate(payload: dict[str, object], context: MigrationContext) -> MigrationOutcome:
    return classify_and_migrate(payload, context, source_schema=SOURCE_SCHEMA, target_schema=TARGET_SCHEMA, preserved={"duration_minutes", "source_id", "learner_level", "lesson_title"}, review_required={"cefr_inferred"}, rejected={"unsupported_source_claim"}, transformed={})
