# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: routes.py
# Description: Connect muscle group URLs to their controller actions.

from app.muscle_group import muscle_group_bp
from app.muscle_group.muscle_group_controller import MuscleGroupController


@muscle_group_bp.route("/muscle-groups")
def list_muscle_groups():
    return MuscleGroupController.list_muscle_groups()
