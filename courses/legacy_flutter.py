"""Dedicated module boundary for the existing flutter curriculum."""
def load(python_course, legacy_courses):
    return next((c for c in legacy_courses if c.get("slug")=="flutter"),None)
