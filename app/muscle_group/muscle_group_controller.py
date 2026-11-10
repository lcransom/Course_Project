from flask import render_template

from app.muscle_group import muscle_group_bp
from app.muscle_group.muscle_group_exceptions import MuscleGroupDataError
from app.muscle_group.muscle_group_manager import get_all_muscle_groups


@muscle_group_bp.route("/muscle-groups")
def list_muscle_groups():
    try:
        muscle_groups = get_all_muscle_groups()
        error_message = None
    except MuscleGroupDataError as error:
        muscle_groups = []
        error_message = str(error)

    return render_template("muscle_group_list.html",muscle_groups=muscle_groups,error_message=error_message)
