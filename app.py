from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///strength_training.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# defining tables that store muscle groups, equipment, and exercises.
class MuscleGroup(db.Model):
    muscle_group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    target_region = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)

    exercises = db.relationship("Exercise", back_populates="muscle_group")


class Equipment(db.Model):
    equipment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category = db.Column(db.String(80), nullable=False)
    target_muscle_focus = db.Column(db.String(120), nullable=False)


class Exercise(db.Model):
    exercise_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    muscle_group_id = db.Column(
        db.Integer, db.ForeignKey("muscle_group.muscle_group_id"), nullable=False
    )
    name = db.Column(db.String(100), nullable=False, unique=True)
    mechanic_type = db.Column(db.String(40), nullable=False)
    difficulty_level = db.Column(db.String(40), nullable=False)

    muscle_group = db.relationship("MuscleGroup", back_populates="exercises")
    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise"
    )


# This table stores each workout.
class WorkoutSession(db.Model):
    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_date = db.Column(db.Date, nullable=False)
    session_rating = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    photo_path = db.Column(db.String(255))

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout_session"
    )


# This table connects workouts to the exercises done in them.
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


@app.get("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
