"""Deterministic production entrypoint for LearnPython."""
import sys
from app import APP

import mysql_adapter
mysql_adapter.install(sys.modules["app"])

import platform_upgrade
platform_upgrade.install()

# The Flask app is now fully configured before Gunicorn starts serving requests.
