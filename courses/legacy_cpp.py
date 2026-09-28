"""Dedicated module boundary for the existing cpp curriculum."""
def load(python_course, legacy_courses):
    return python_course if "cpp"=="python" else next((c for c in legacy_courses if c.get("slug")=="cpp"),None)
