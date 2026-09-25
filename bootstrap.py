"""Deterministic production entrypoint for LearnPython."""
import sys
from app import APP

import mysql_adapter
mysql_adapter.install(sys.modules["app"])

import platform_upgrade
\n# Railway serves the app over HTTPS. Force secure host-only sessions so login\n# survives redirects and browsers do not reject the __Host-session cookie.\nAPP.config["SESSION_COOKIE_SECURE"] = True\nAPP.config["SESSION_COOKIE_NAME"] = "__Host-session"\n\n# Install the platform UI before Gunicorn begins serving requests.\nplatform_upgrade.install()

# The Flask app is now fully configured before Gunicorn starts serving requests.
