# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: equipment_manager.py
# Description: Retrieve all equipment or filter records by category.

from sqlalchemy.exc import SQLAlchemyError

from app.equipment.equipment_exceptions import EquipmentDataError
from app.equipment.models import Equipment
from extensions import db


def get_all_equipment(category=None, sort_by="name", sort_order="asc", limit=None):
    try:
        query = Equipment.query
        sort_columns = {
            "name": Equipment.name,
            "category": Equipment.category,
            "target_muscle_focus": Equipment.target_muscle_focus,
        }
        if category:
            query = query.filter(Equipment.category == category)

        sort_column = sort_columns.get(sort_by, Equipment.name)
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        if limit is not None:
            query = query.limit(limit)

        return query.all()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise EquipmentDataError(
            "Equipment could not be loaded. Please try again later."
        ) from error
