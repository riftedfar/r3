"""Production entrypoint for LearnPython on Railway.

Loads the database adapter and platform route/UI layer before Gunicorn starts.
"""
import sys

from app import APP

import mysql_adapter
mysql_adapter.install(sys.modules["app"])

import platform_upgrade
platform_upgrade.install()
