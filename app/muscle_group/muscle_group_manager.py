# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: muscle_group_manager.py
# Description: Retrieve and search muscle group records and handle database errors.

from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError

from app.muscle_group.models import MuscleGroup
from app.muscle_group.muscle_group_exceptions import MuscleGroupDataError
from extensions import db


def get_all_muscle_groups():
    # Load all muscle groups for the list page.
    try:
        return MuscleGroup.query.all()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise MuscleGroupDataError("Muscle groups could not be loaded. Please try again later.") from error


def search_muscle_groups(search_query):
    """Search muscle groups using multiple terms combined with AND logic."""
    if not search_query or not search_query.strip():
        return get_all_muscle_groups()

    # Sanitize and split the search string into individual terms
    terms = [term.strip() for term in search_query.split() if term.strip()]

    if not terms:
        return get_all_muscle_groups()

    try:
        # Start with a base query
        query = MuscleGroup.query

        # Build the search conditions using .like() with wildcards
        # For each term, it must match the name, region, OR description
        # Because we use and_(*conditions), the results must match ALL terms provided.
        conditions = [
            or_(
                MuscleGroup.name.like(f"%{term}%"),
                MuscleGroup.target_region.like(f"%{term}%"),
                MuscleGroup.description.like(f"%{term}%")
            ) for term in terms
        ]

        # Execute the query with the built conditions
        return query.filter(and_(*conditions)).all()

    except SQLAlchemyError as error:
        db.session.rollback()
        raise MuscleGroupDataError("Search results could not be loaded. Please try again later.") from error