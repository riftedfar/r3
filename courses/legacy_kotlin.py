"""Dedicated module boundary for the existing kotlin curriculum."""
def load(python_course, legacy_courses):
    return python_course if "kotlin"=="python" else next((c for c in legacy_courses if c.get("slug")=="kotlin"),None)
