# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: muscle_group_controller.py
# Description: Load muscle group data and render the muscle group page.

from flask import render_template

from app.muscle_group.muscle_group_manager import get_all_muscle_groups


class MuscleGroupController:
    @staticmethod
    def list_muscle_groups():
        muscle_groups = get_all_muscle_groups()
        return render_template(
            "muscle_group_list.html", muscle_groups=muscle_groups
        )
