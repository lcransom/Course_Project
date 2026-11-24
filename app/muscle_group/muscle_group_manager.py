# Authors: Levi Ransom, Roger Major, Rithik Saini
# Date: 11/17/2026
# File: muscle_group_manager.py
# Description: Retrieve and search muscle group records and handle database errors.

from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.core.models import Exercise
from app.muscle_group.models import MuscleGroup
from app.muscle_group.muscle_group_exceptions import MuscleGroupDataError
from extensions import db


# --- CENTRALIZED EXCEPTION HANDLER ---
def _handle_query_error(action, error):
    """Centralized error handler for all muscle group database operations."""
    db.session.rollback()
    raise MuscleGroupDataError(
        f"Muscle groups could not be {action}. Please try again later."
    ) from error


def get_all_muscle_groups():
    # Load related exercises and equipment with the muscle groups so the
    # template can display the relationships without issuing extra queries.
    try:
        statement = db.select(MuscleGroup).options(
            selectinload(MuscleGroup.exercises).joinedload(Exercise.equipment)
        )
        return db.session.scalars(statement).all()
    except SQLAlchemyError as error:
        _handle_query_error("loaded", error)


def search_muscle_groups(search_query):
    """Search muscle groups using multiple terms combined with AND logic."""
    if not search_query or not search_query.strip():
        return get_all_muscle_groups()

    # Split the search string into individual terms.
    terms = [term.strip() for term in search_query.split() if term.strip()]

    if not terms:
        return get_all_muscle_groups()

    try:
        # Load each muscle group's exercises and each exercise's equipment.
        statement = db.select(MuscleGroup).options(
            selectinload(MuscleGroup.exercises).joinedload(Exercise.equipment)
        )

        # Each term must match the name, region, or description.
        conditions = [
            or_(
                MuscleGroup.name.like(f"%{term}%"),
                MuscleGroup.target_region.like(f"%{term}%"),
                MuscleGroup.description.like(f"%{term}%"),
            )
            for term in terms
        ]

        statement = statement.where(and_(*conditions))
        return db.session.scalars(statement).all()

    except SQLAlchemyError as error:
        _handle_query_error("searched", error)