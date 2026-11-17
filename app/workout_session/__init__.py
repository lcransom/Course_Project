# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: __init__.py

from flask import Blueprint

workout_session_bp = Blueprint(
    "workout_session",
    __name__,
    template_folder="templates",
    static_folder="static",
)
