# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: muscle_group_controller.py
# Description: Load and search muscle group data and render the muscle group page.

from flask import render_template, request

from app.muscle_group.muscle_group_manager import search_muscle_groups


class MuscleGroupController:
    @staticmethod
    def list_muscle_groups():
        # Grab the 'search' parameter from the URL (e.g., /muscle-groups?search=upper)
        search_query = request.args.get("search", "").strip()

        try:
            # Call the search manager (which falls back to all records if query is empty)
            muscle_groups = search_muscle_groups(search_query)

            return render_template(
                "muscle_group_list.html",
                muscle_groups=muscle_groups,
                search_query=search_query
            )
        except Exception as e:

            raise