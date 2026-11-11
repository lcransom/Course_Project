from flask import render_template
from app.workout_session import workout_session_bp
from app.workout_session.workout_exceptions import WorkoutDataError
from app.workout_session.workout_manager import get_all_workout_sessions

@workout_session_bp.route("/workouts")
def list_workouts():
    try:
        workouts = get_all_workout_sessions()
        error_message = None
    except WorkoutDataError as error:
        workouts = []
        error_message = str(error)

    return render_template("workout_list.html", workouts=workouts, error_message=error_message)