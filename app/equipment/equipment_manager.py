# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: equipment_manager.py
# Description: Retrieve equipment with optional category filtering, sorting, and limits.

from sqlalchemy.exc import SQLAlchemyError

from app.equipment.equipment_exceptions import EquipmentDataError
from app.equipment.models import Equipment
from extensions import db


def get_all_equipment(category=None, sort_by="name", sort_order="asc", limit=None):
    try:
        statement = db.select(Equipment)
        # Allow only known model columns so URL input cannot select arbitrary sort fields.
        sort_columns = {
            "name": Equipment.name,
            "category": Equipment.category,
            "target_muscle_focus": Equipment.target_muscle_focus,
        }
        if category:
            # Apply the category filter before sorting and limiting the results.
            statement = statement.where(Equipment.category == category)

        sort_column = (
            sort_columns[sort_by] if sort_by in sort_columns else Equipment.name
        )
        if sort_order == "desc":
            statement = statement.order_by(sort_column.desc())
        else:
            statement = statement.order_by(sort_column.asc())
        if limit is not None:
            # Limit the final filtered and sorted result set.
            statement = statement.limit(limit)

        return db.session.scalars(statement).all()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise EquipmentDataError(
            "Equipment could not be loaded. Please try again later."
        ) from error
