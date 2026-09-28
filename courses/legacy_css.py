"""Dedicated module boundary for the existing css curriculum."""
def load(python_course, legacy_courses):
    return python_course if "css"=="python" else next((c for c in legacy_courses if c.get("slug")=="css"),None)
