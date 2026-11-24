# Authors: Levi Ransom, Roger Major, Rithik Saini
# Date: 11/17/2026
# File: muscle_group_controller.py
# Description: Load muscle group data and render the muscle group page.

from flask import render_template, request

from app.muscle_group.muscle_group_manager import MuscleGroupManager


class MuscleGroupController:
    @staticmethod
    def list_muscle_groups():
        search_query = request.args.get("search", "").strip()
        muscle_groups = MuscleGroupManager.search_muscle_groups(search_query)
        return render_template(
            "muscle_group_list.html",
            muscle_groups=muscle_groups,
            search_query=search_query,
        )