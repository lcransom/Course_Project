# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: equipment_manager.py
# Description: Retrieve all equipment or filter records by category.

from sqlalchemy.exc import SQLAlchemyError

from app.equipment.equipment_exceptions import EquipmentDataError
from app.equipment.models import Equipment
from extensions import db


# --- CENTRALIZED EXCEPTION HANDLER ---
def _handle_query_error(error):
    """Centralized error handler for all equipment database operations."""
    db.session.rollback()
    raise EquipmentDataError(
        "Equipment could not be loaded. Please try again later."
    ) from error


def get_all_equipment(category=None, sort_by="name", sort_order="asc", limit=None):
    try:
        statement = db.select(Equipment)
        sort_columns = {
            "name": Equipment.name,
            "category": Equipment.category,
            "target_muscle_focus": Equipment.target_muscle_focus,
        }

        # Apply filtering
        if category:
            statement = statement.where(Equipment.category == category)

        # Apply sorting
        sort_column = sort_columns.get(sort_by, Equipment.name)
        if sort_order == "desc":
            statement = statement.order_by(sort_column.desc())
        else:
            statement = statement.order_by(sort_column.asc())

        # Apply limiting
        if limit is not None:
            statement = statement.limit(limit)

        # Execute the statement
        return db.session.scalars(statement).all()
    except SQLAlchemyError as error:
        _handle_query_error(error)