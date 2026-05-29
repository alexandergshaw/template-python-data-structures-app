"""Vercel serverless function entrypoint.

Exposes the Flask application as a WSGI handler that Vercel's
Python runtime can invoke.
"""

from app import create_app

app = create_app("production")
