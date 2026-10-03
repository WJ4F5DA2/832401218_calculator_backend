"""Application entry point.

Starts the Flask server for the calculator back end.
On platforms like Render, the port is provided through the PORT
environment variable; locally it defaults to 5000.
"""
import os

from src.app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
