# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: __init__.py

from flask import Blueprint

equipment_bp = Blueprint(
    "equipment", __name__, template_folder="templates", static_folder="static"
)
