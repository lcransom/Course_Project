# Authors: Levi Ransom, Roger Major, Rithik Saini
# Date: 11/17/2026
# File: muscle_group_manager.py
# Description: Retrieve and search muscle group records and handle database errors.

from typing import NoReturn

from flask import abort
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.core.models import Exercise
from app.muscle_group.models import MuscleGroup
from app.muscle_group.muscle_group_exceptions import MuscleGroupDataError
from extensions import db


class MuscleGroupManager:

    @staticmethod
    def get_all_muscle_groups():
        try:
            statement = db.select(MuscleGroup).options(
                selectinload(MuscleGroup.exercises).joinedload(Exercise.equipment)
            )
            return db.session.scalars(statement).all()
        except Exception as e:
            MuscleGroupManager.handle_exceptions(e)

    @staticmethod
    def search_muscle_groups(search_query):
        """Search muscle groups using multiple terms combined with AND logic."""
        if not search_query or not search_query.strip():
            return MuscleGroupManager.get_all_muscle_groups()

        terms = [term.strip() for term in search_query.split() if term.strip()]

        if not terms:
            return MuscleGroupManager.get_all_muscle_groups()

        try:
            statement = db.select(MuscleGroup).options(
                selectinload(MuscleGroup.exercises).joinedload(Exercise.equipment)
            )

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
        except Exception as e:
            MuscleGroupManager.handle_exceptions(e)

            @staticmethod
            def handle_exceptions(e) -> NoReturn:
                """Centralized exception handler for the Muscle Group domain."""
                db.session.rollback()
                if isinstance(e, MuscleGroupDataError):
                    abort(500, description=str(e))
                elif isinstance(e, SQLAlchemyError):
                    abort(500, description=f"A database error has occurred: {str(e)}")
                else:
                    abort(500, description=str(e))
