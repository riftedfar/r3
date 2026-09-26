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
seo_routes.install(APP, sys.modules["app"], APP.layout)
