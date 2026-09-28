"""Dedicated module boundary for the existing bash-linux curriculum."""
def load(python_course, legacy_courses):
    return next((c for c in legacy_courses if c.get("slug")=="bash-linux"),None)
