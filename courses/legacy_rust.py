"""Dedicated module boundary for the existing rust curriculum."""
def load(python_course, legacy_courses):
    return python_course if "rust"=="python" else next((c for c in legacy_courses if c.get("slug")=="rust"),None)
