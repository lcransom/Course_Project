# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: __init__.py
# Description: Create the Flask application, register routes, and configure error handling.

from flask import Flask, render_template
from sqlalchemy.exc import SQLAlchemyError

from database import initialize_database
from extensions import db


def create_app():
    app = Flask(__name__)
    initialize_database(app)

    from app.muscle_group.models import MuscleGroup
    from app.equipment.models import Equipment
    from app.workout_session.models import WorkoutSession
    from app.core.models import Exercise, WorkoutExercise

    from app.muscle_group import muscle_group_bp
    from app.equipment import equipment_bp
    from app.workout_session import workout_session_bp
    from app.muscle_group import routes as muscle_group_routes
    from app.equipment import routes as equipment_routes
    from app.workout_session import routes as workout_routes

    app.register_blueprint(muscle_group_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(workout_session_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    from app.equipment.equipment_exceptions import EquipmentDataError
    from app.muscle_group.muscle_group_exceptions import MuscleGroupDataError
    from app.workout_session.workout_exceptions import WorkoutDataError

    @app.errorhandler(SQLAlchemyError)
    @app.errorhandler(EquipmentDataError)
    @app.errorhandler(MuscleGroupDataError)
    @app.errorhandler(WorkoutDataError)
    def handle_data_error(error):
        db.session.rollback()
        app.logger.exception("Unhandled data access error")
        return render_template("500.html"), 500

    with app.app_context():
        db.create_all()

    return app
