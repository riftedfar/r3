"""Production entrypoint for LearnPython on Railway.

Loads the database adapter and platform route/UI layer before Gunicorn starts.
"""
import sys

from app import APP

import mysql_adapter
mysql_adapter.install(sys.modules["app"])

import platform_upgrade
platform_upgrade.install()

# SEO, crawl directives, social metadata, and custom 404.
import seo_routes
from additional_courses import COURSES as EXTRA_COURSES

def seo_courses():
    py={"slug":"python","title":"Python","tag":"PYTHON","description":"The complete Python learning path.","lessons":sys.modules["app"].COURSE,"href":"/courses/python"}
    extras=[{"slug":c["slug"],"title":c["title"],"tag":c["tag"],"description":c["description"],"lessons":c["lessons"],"href":"/courses/"+c["slug"]} for c in EXTRA_COURSES]
    return [py]+extras

seo_routes.install(APP, sys.modules["app"], seo_courses, sys.modules["app"].layout)
