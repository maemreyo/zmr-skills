from enum import StrEnum


class Materiality(StrEnum):
    NON_MATERIAL = "non_material"
    MATERIAL = "material"


_NON_MATERIAL = {"metadata", "spacing", "response_box_geometry", "alt_text", "title"}
_MATERIAL = {"objective", "source_substitution", "scoring_membership", "grammar_scope", "privacy_model", "assessment_construct"}


def classify_materiality(change_kinds: tuple[str, ...]) -> Materiality:
    if any(kind in _MATERIAL for kind in change_kinds):
        return Materiality.MATERIAL
    if all(kind in _NON_MATERIAL for kind in change_kinds):
        return Materiality.NON_MATERIAL
    return Materiality.MATERIAL
