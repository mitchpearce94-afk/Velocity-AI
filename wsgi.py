"""
WSGI entry point for Railway deployment.
Imports the Flask app from webhook-server.py (which has a hyphenated filename).

NOTE: The email templates directory was renamed from email/ to emails/ to avoid
shadowing Python's built-in 'email' module.
"""
import importlib
import sys
import os

# Add operations/ to the path so webhook-server can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "operations"))

# Import the Flask app using importlib (since 'webhook-server' has a hyphen)
webhook_server = importlib.import_module("webhook-server")
app = webhook_server.app
