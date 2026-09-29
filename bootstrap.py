"""Production entrypoint for EaseWithPy on Railway."""
import sys
from app import APP

import mysql_adapter
mysql_adapter.install(sys.modules["app"])

import platform_upgrade
platform_upgrade.install()

import seo_routes
from additional_courses import COURSES as LEGACY_EXTRA_COURSES
from course_registry import extra_courses
EXTRA_COURSES = extra_courses(sys.modules["app"].COURSE, LEGACY_EXTRA_COURSES)

def seo_courses():
    py={"slug":"python","title":"Python","tag":"PYTHON","description":"The complete Python learning path.","lessons":sys.modules["app"].COURSE,"href":"/courses/python"}
    extras=[{"slug":c["slug"],"title":c["title"],"tag":c["tag"],"description":c["description"],"lessons":c["lessons"],"href":"/courses/"+c["slug"]} for c in EXTRA_COURSES]
    return [py]+extras

seo_routes.install(APP, sys.modules["app"], seo_courses, sys.modules["app"].layout)

import academy_expansion
academy_expansion.install()

import learning_features
learning_features.install()

import learning_extras
learning_extras.install()

# Final launch-readiness layer: hands-on exercises, autosave, feedback, security
# headers, friendly production errors, legal pages and launch diagnostics.
import launch_readiness
launch_readiness.install()
