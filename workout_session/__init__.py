from flask import Blueprint

workout_session_bp = Blueprint("workout_session", __name__, template_folder="templates", static_folder="static")
