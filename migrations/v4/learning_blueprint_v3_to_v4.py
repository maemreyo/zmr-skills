from __future__ import annotations
from zamery_education_v4.kernel.migrations.runner import MigrationContext
from zamery_education_v4.kernel.records.migration import MigrationOutcome
from ._common import classify_and_migrate
SOURCE_SCHEMA = "learning-blueprint.v3"
TARGET_SCHEMA = "learning-blueprint.v4"
def migrate(payload: dict[str, object], context: MigrationContext) -> MigrationOutcome:
    return classify_and_migrate(payload, context, source_schema=SOURCE_SCHEMA, target_schema=TARGET_SCHEMA, preserved={"objectives", "stages", "duration_minutes"}, review_required={"progression_labels"}, rejected=set(), transformed={})
