from extensions import db

class Equipment(db.Model):
    __tablename__ = "equipment"
    equipment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category = db.Column(db.String(80), nullable=False)
    target_muscle_focus = db.Column(db.String(120), nullable=False)

    # Relationship to Exercise (string reference avoids circular import)
    exercises = db.relationship("Exercise", back_populates="equipment")