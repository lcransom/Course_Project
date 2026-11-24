# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: workout_manager.py
# Description: Retrieve workout sessions and handle database read errors.

from typing import NoReturn

from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from app.workout_session.models import WorkoutSession
from app.workout_session.workout_exceptions import WorkoutDataError
from extensions import db


class WorkoutManager:

    @staticmethod
    def get_all_workout_sessions():
        try:
            statement = db.select(WorkoutSession).order_by(
                WorkoutSession.workout_date.desc()
            )
            return db.session.scalars(statement).all()
        except Exception as e:
            WorkoutManager.handle_exceptions(e)

    @staticmethod
    def handle_exceptions(e) -> NoReturn:
        """Centralized exception handler for the Workout Session domain."""
        db.session.rollback()
        if isinstance(e, WorkoutDataError):
            abort(500, description=str(e))
        elif isinstance(e, SQLAlchemyError):
            abort(500, description=f"A database error has occurred: {str(e)}")
        else:
            abort(500, description=str(e))