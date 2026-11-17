# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: routes.py
# Description: Connect workout session URLs to their controller actions.

from app.workout_session import workout_session_bp
from app.workout_session.workout_controller import WorkoutController


@workout_session_bp.route("/workouts")
def list_workouts():
    return WorkoutController.list_workouts()
