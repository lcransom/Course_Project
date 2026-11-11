from extensions import db

class Exercise(db.Model):
    __tablename__ = "exercise"
    exercise_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    muscle_group_id = db.Column(db.Integer, db.ForeignKey("muscle_group.muscle_group_id"), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.equipment_id"), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    mechanic_type = db.Column(db.String(40), nullable=False)
    difficulty_level = db.Column(db.String(40), nullable=False)

    muscle_group = db.relationship("MuscleGroup", back_populates="exercises")
    equipment = db.relationship("Equipment", back_populates="exercises")
    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise")

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercise"
    workout_exercise_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workout_session.workout_id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.exercise_id"), nullable=False)
    sets_completed = db.Column(db.Integer, nullable=False)
    target_reps = db.Column(db.Integer, nullable=False)
    weight_used = db.Column(db.Float, nullable=False)

    workout_session = db.relationship("WorkoutSession", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")
