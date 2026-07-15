from __future__ import annotations

from zamery_education_v4.kernel.migrations import MigrationDefinition, MigrationRegistry

from . import (
    deck_manifest_v3_to_v4,
    layout_manifest_v3_to_v4,
    learning_blueprint_v3_to_v4,
    pack_manifest_v3_to_v4,
    practice_content_v3_to_v4,
    teaching_brief_v3_to_v4,
)


def default_v3_registry() -> MigrationRegistry:
    registry = MigrationRegistry()
    modules = (
        teaching_brief_v3_to_v4,
        learning_blueprint_v3_to_v4,
        practice_content_v3_to_v4,
        deck_manifest_v3_to_v4,
        layout_manifest_v3_to_v4,
        pack_manifest_v3_to_v4,
    )
    for module in modules:
        registry.register(
            MigrationDefinition(module.SOURCE_SCHEMA, module.TARGET_SCHEMA, module.migrate)
        )
    return registry
