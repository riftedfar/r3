"""Dedicated module boundary for the existing html curriculum."""
def load(python_course, legacy_courses):
    return python_course if "html"=="python" else next((c for c in legacy_courses if c.get("slug")=="html"),None)
