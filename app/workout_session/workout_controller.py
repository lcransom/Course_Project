# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: workout_controller.py

from flask import render_template

from app.workout_session.workout_manager import get_all_workout_sessions


class WorkoutController:
    @staticmethod
    def list_workouts():
        workouts = get_all_workout_sessions()
        return render_template("workout_list.html", workouts=workouts)
