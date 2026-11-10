from flask import Flask

from database import initialize_database
from extensions import db

# Import the model so SQLAlchemy knows about its table.
from app.muscle_group.models import MuscleGroup
from app.muscle_group import muscle_group_bp
from app.muscle_group import muscle_group_controller

# Create the Flask app.
app = Flask(__name__)
initialize_database(app)
app.register_blueprint(muscle_group_bp)


# Store information about gym equipment.
class Equipment(db.Model):
    equipment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category = db.Column(db.String(80), nullable=False)
    target_muscle_focus = db.Column(db.String(120), nullable=False)

    exercises = db.relationship("Exercise", back_populates="equipment")


# Store exercises and their muscle group and equipment.
class Exercise(db.Model):
    exercise_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    muscle_group_id = db.Column(
        db.Integer, db.ForeignKey("muscle_group.muscle_group_id"), nullable=False
    )
    equipment_id = db.Column(
        db.Integer, db.ForeignKey("equipment.equipment_id"), nullable=False
    )
    name = db.Column(db.String(100), nullable=False, unique=True)
    mechanic_type = db.Column(db.String(40), nullable=False)
    difficulty_level = db.Column(db.String(40), nullable=False)

    muscle_group = db.relationship("MuscleGroup", back_populates="exercises")
    equipment = db.relationship("Equipment", back_populates="exercises")
    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise"
    )


# Store information about one workout session.
class WorkoutSession(db.Model):
    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_date = db.Column(db.Date, nullable=False)
    session_rating = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    photo_path = db.Column(db.String(255))

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout_session"
    )


# Connect a workout to its exercises and record sets, reps, and weight.
class WorkoutExercise(db.Model):
    workout_exercise_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    workout_id = db.Column(
        db.Integer, db.ForeignKey("workout_session.workout_id"), nullable=False
    )
    exercise_id = db.Column(
        db.Integer, db.ForeignKey("exercise.exercise_id"), nullable=False
    )
    sets_completed = db.Column(db.Integer, nullable=False)
    target_reps = db.Column(db.Integer, nullable=False)
    weight_used = db.Column(db.Float, nullable=False)

    workout_session = db.relationship(
        "WorkoutSession", back_populates="workout_exercises"
    )
    exercise = db.relationship("Exercise", back_populates="workout_exercises")


@app.route("/")
def workout_pag():
    return "Workout page"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
