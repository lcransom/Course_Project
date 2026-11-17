# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: models.py

from extensions import db


class Equipment(db.Model):
    __tablename__ = "equipment"

    equipment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category = db.Column(db.String(80), nullable=False)
    target_muscle_focus = db.Column(db.String(120), nullable=False)

    exercises = db.relationship("Exercise", back_populates="equipment")
