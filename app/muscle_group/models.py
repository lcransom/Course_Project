from extensions import db


class MuscleGroup(db.Model):
    # This table stores information about a muscle group.
    __tablename__ = "muscle_group"

    muscle_group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    target_region = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)

    exercises = db.relationship("Exercise", back_populates="muscle_group")
