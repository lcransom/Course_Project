# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: models.py
# Description: Define the workout session database model and its exercises relationship.

from extensions import db


class WorkoutSession(db.Model):
    __tablename__ = "workout_session"

    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_date = db.Column(db.Date, nullable=False)
    session_rating = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    photo_path = db.Column(db.String(255))

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout_session"
    )
