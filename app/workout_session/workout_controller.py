# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: workout_controller.py
# Description: Load workout session data and render the workout page.

from flask import render_template

from app.workout_session.workout_manager import WorkoutManager


class WorkoutController:
    @staticmethod
    def list_workouts():
        workouts = WorkoutManager.get_all_workout_sessions()
        return render_template("workout_list.html", workouts=workouts)