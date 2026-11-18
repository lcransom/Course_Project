# Authors: Levi Ransom, Roger Major, Rithik Saini
# Date: 11/17/2026
# File: muscle_group_manager.py
# Description: Retrieve and search muscle group records and handle database errors.

from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

from app.core.models import Exercise
from app.muscle_group.models import MuscleGroup
from app.muscle_group.muscle_group_exceptions import MuscleGroupDataError
from extensions import db


def get_all_muscle_groups():
    # Load related exercises and equipment with the muscle groups so the
    # template can display the relationships without issuing extra queries.
    try:
        return (
            MuscleGroup.query.options(
                selectinload(MuscleGroup.exercises).joinedload(Exercise.equipment)
            )
            .all()
        )
    except SQLAlchemyError as error:
        db.session.rollback()
        raise MuscleGroupDataError(
            "Muscle groups could not be loaded. Please try again later."
        ) from error


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
        query = MuscleGroup.query.options(
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

        return query.filter(and_(*conditions)).all()

    except SQLAlchemyError as error:
        db.session.rollback()
        raise MuscleGroupDataError(
            "Search results could not be loaded. Please try again later."
        ) from error
