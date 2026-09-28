"""Dedicated module boundary for the existing go curriculum."""
def load(python_course, legacy_courses):
    return python_course if "go"=="python" else next((c for c in legacy_courses if c.get("slug")=="go"),None)
