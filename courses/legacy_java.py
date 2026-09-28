"""Dedicated module boundary for the existing java curriculum."""
def load(python_course, legacy_courses):
    return python_course if "java"=="python" else next((c for c in legacy_courses if c.get("slug")=="java"),None)
