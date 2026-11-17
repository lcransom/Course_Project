# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: routes.py

from app.equipment import equipment_bp
from app.equipment.equipment_controller import EquipmentController


@equipment_bp.route("/equipment")
def list_equipment():
    return EquipmentController.list_equipment()
