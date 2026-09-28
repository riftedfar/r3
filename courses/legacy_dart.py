"""Dedicated module boundary for the existing dart curriculum."""
def load(python_course, legacy_courses):
    return python_course if "dart"=="python" else next((c for c in legacy_courses if c.get("slug")=="dart"),None)
