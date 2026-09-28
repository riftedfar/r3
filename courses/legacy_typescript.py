"""Dedicated module boundary for the existing typescript curriculum."""
def load(python_course, legacy_courses):
    return python_course if "typescript"=="python" else next((c for c in legacy_courses if c.get("slug")=="typescript"),None)
