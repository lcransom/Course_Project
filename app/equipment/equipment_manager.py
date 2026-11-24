# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: equipment_manager.py
# Description: Retrieve all equipment or filter records by category.

from typing import NoReturn

from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from app.equipment.equipment_exceptions import EquipmentDataError
from app.equipment.models import Equipment
from extensions import db


class EquipmentManager:

    @staticmethod
    def get_all_equipment(category=None, sort_by="name", sort_order="asc", limit=None):
        try:
            statement = db.select(Equipment)
            sort_columns = {
                "name": Equipment.name,
                "category": Equipment.category,
                "target_muscle_focus": Equipment.target_muscle_focus,
            }
            if category:
                statement = statement.where(Equipment.category == category)

            sort_column = sort_columns.get(sort_by, Equipment.name)
            if sort_order == "desc":
                statement = statement.order_by(sort_column.desc())
            else:
                statement = statement.order_by(sort_column.asc())

            if limit is not None:
                statement = statement.limit(limit)

            return db.session.scalars(statement).all()
        except Exception as e:
            EquipmentManager.handle_exceptions(e)

            @staticmethod
            def handle_exceptions(e) -> NoReturn:
                """Centralized exception handler for the Equipment domain."""
                db.session.rollback()
                if isinstance(e, EquipmentDataError):
                    abort(500, description=str(e))
                elif isinstance(e, SQLAlchemyError):
                    abort(500, description=f"A database error has occurred: {str(e)}")
                else:
                    abort(500, description=str(e))

