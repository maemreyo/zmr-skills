TEACHER_ONLY_SCOPES = {"teaching_brief", "pedagogy", "content", "publication"}


def role_can_approve(role: str, scope: str) -> bool:
    if scope in TEACHER_ONLY_SCOPES:
        return role in {"teacher", "lead_teacher", "administrator"}
    return role in {"teacher", "lead_teacher", "administrator", "reviewer"}
