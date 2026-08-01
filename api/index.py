from api import create_app

# Expose the Flask app for Vercel's Python serverless runtime
app = create_app()

# Vercel expects a callable named `handler` for Python functions.
# This wrapper forwards the WSGI request to the Flask app.
def handler(request, response):
    return app(request.environ, start_response=response.start)
