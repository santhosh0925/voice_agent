from api import create_app

# Vercel's Python runtime serves Flask through WSGI when a top-level
# `app` object is exported from the function file.
app = create_app()
