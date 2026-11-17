# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: equipment_manager.py

from sqlalchemy.exc import SQLAlchemyError

from app.equipment.equipment_exceptions import EquipmentDataError
from app.equipment.models import Equipment
from extensions import db


def get_all_equipment():
    try:
        return Equipment.query.all()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise EquipmentDataError(
            "Equipment could not be loaded. Please try again later."
        ) from error
