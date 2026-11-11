from sqlalchemy.exc import SQLAlchemyError
from app.equipment.models import Equipment
from app.equipment.equipment_exceptions import EquipmentDataError
from extensions import db

def get_all_equipment():
    try:
        return Equipment.query.all()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise EquipmentDataError("Equipment could not be loaded. Please try again later.") from error
