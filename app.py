# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: app.py
# Description: Start the FitTrack Flask application.

from app import create_app


app = create_app()


if __name__ == "__main__":
    app.run()
