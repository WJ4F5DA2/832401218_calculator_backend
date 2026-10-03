"""Flask application factory for the calculator back end."""
from flask import Flask

from src.controller.routes import bp
from src.model.database import init_db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    init_db()

    # Simple CORS headers so the front end can call the API from any origin.
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, DELETE, OPTIONS"
        )
        return response

    app.register_blueprint(bp)
    return app
