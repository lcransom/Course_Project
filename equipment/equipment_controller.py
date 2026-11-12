from flask import render_template
from app.equipment import equipment_bp
from app.equipment.equipment_exceptions import EquipmentDataError
from app.equipment.equipment_manager import get_all_equipment

@equipment_bp.route("/equipment")
def list_equipment():
    try:
        equipment_list = get_all_equipment()
        error_message = None
    except EquipmentDataError as error:
        equipment_list = []
        error_message = str(error)

    return render_template("equipment_list.html", equipment=equipment_list, error_message=error_message)