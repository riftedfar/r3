"""Dedicated module boundary for the existing ai curriculum."""
def load(python_course, legacy_courses):
    return python_course if "ai"=="python" else next((c for c in legacy_courses if c.get("slug")=="ai"),None)
