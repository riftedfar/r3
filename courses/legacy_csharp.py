"""Dedicated module boundary for the existing csharp curriculum."""
def load(python_course, legacy_courses):
    return python_course if "csharp"=="python" else next((c for c in legacy_courses if c.get("slug")=="csharp"),None)
