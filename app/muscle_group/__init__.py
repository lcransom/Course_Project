# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: __init__.py
# Description: Define and configure the muscle group Blueprint.

from flask import Blueprint

muscle_group_bp = Blueprint(
    "muscle_group", __name__, template_folder="templates", static_folder="static"
)
