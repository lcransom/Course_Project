# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: equipment_controller.py

from flask import render_template

from app.equipment.equipment_manager import get_all_equipment


class EquipmentController:
    @staticmethod
    def list_equipment():
        equipment = get_all_equipment()
        return render_template("equipment_list.html", equipment=equipment)
