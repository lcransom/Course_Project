# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: equipment_controller.py
# Description: Handle equipment page requests and pass filter and sorting options to the manager.
from flask import render_template, request

from app.equipment.equipment_manager import get_all_equipment


class EquipmentController:
    @staticmethod
    def list_equipment():
        # Read the filter and sort choices submitted as URL query parameters.
        category = request.args.get("category", "").strip()
        sort_by = request.args.get("sort_by", "name").strip().lower()
        sort_order = request.args.get("sort_order", "asc").strip().lower()
        limit_value = request.args.get("limit", "").strip()

        valid_sort_fields = {"name", "category", "target_muscle_focus"}
        valid_sort_orders = {"asc", "desc"}
        if sort_by not in valid_sort_fields or sort_order not in valid_sort_orders:
            return render_template(
                "equipment_list.html",
                equipment=[],
                error_message="Choose a valid sort field and order.",
            )

        try:
            # A blank limit means no limit; reject values that are not positive integers.
            limit = int(limit_value) if limit_value else None
            if limit is not None and limit <= 0:
                raise ValueError
        except ValueError:
            return render_template(
                "equipment_list.html",
                equipment=[],
                error_message="Result limit must be a positive whole number.",
            )

        equipment = get_all_equipment(
            category or None,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
        )
        return render_template("equipment_list.html", equipment=equipment)
