# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: workout_manager.py

from sqlalchemy.exc import SQLAlchemyError

from app.workout_session.models import WorkoutSession
from app.workout_session.workout_exceptions import WorkoutDataError
from extensions import db


def get_all_workout_sessions():
    try:
        return WorkoutSession.query.order_by(
            WorkoutSession.workout_date.desc()
        ).all()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise WorkoutDataError(
            "Workout sessions could not be loaded. Please try again later."
        ) from error
