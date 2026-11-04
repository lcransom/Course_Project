import sqlite3
import os

# Define the database file path (in the same folder as this script)
DB_PATH = 'fitness.db'


def create_database():
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # --- SCHEMA CREATION ---
    # Drop tables if they exist to allow re-running the script cleanly
    cursor.executescript("""
                         DROP TABLE IF EXISTS WorkoutExercise;
                         DROP TABLE IF EXISTS Exercise;
                         DROP TABLE IF EXISTS WorkoutSession;
                         DROP TABLE IF EXISTS Equipment;
                         DROP TABLE IF EXISTS MuscleGroup;
                         """)

    # Create Tables
    cursor.executescript("""
                         CREATE TABLE MuscleGroup
                         (
                             muscle_group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name            VARCHAR(100) NOT NULL,
                             target_region   VARCHAR(100),
                             description     TEXT
                         );

                         CREATE TABLE Equipment
                         (
                             equipment_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                             name                VARCHAR(100) NOT NULL,
                             category            VARCHAR(50),
                             target_muscle_focus VARCHAR(100)
                         );

                         CREATE TABLE WorkoutSession
                         (
                             workout_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                             workout_date   DATE NOT NULL,
                             session_rating INTEGER CHECK (session_rating BETWEEN 1 AND 5),
                             notes          TEXT,
                             photo_path     VARCHAR(255)
                         );

                         CREATE TABLE Exercise
                         (
                             exercise_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                             muscle_group_id  INTEGER      NOT NULL,
                             name             VARCHAR(100) NOT NULL,
                             mechanic_type    VARCHAR(50),
                             difficulty_level VARCHAR(50),
                             FOREIGN KEY (muscle_group_id) REFERENCES MuscleGroup (muscle_group_id)
                         );

                         CREATE TABLE WorkoutExercise
                         (
                             workout_exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
                             workout_id          INTEGER NOT NULL,
                             exercise_id         INTEGER NOT NULL,
                             sets_completed      INTEGER,
                             target_reps         INTEGER,
                             weight_used         FLOAT,
                             FOREIGN KEY (workout_id) REFERENCES WorkoutSession (workout_id),
                             FOREIGN KEY (exercise_id) REFERENCES Exercise (exercise_id)
                         );
                         """)

    # --- SAMPLE DATA INSERTION ---

    # 1. MuscleGroup (5 rows)
    muscle_groups = [
        ('Chest', 'Upper Body', 'Pectoralis major and minor'),
        ('Back', 'Upper Body', 'Latissimus dorsi, rhomboids, trapezius'),
        ('Legs', 'Lower Body', 'Quadriceps, hamstrings, calves, glutes'),
        ('Shoulders', 'Upper Body', 'Deltoids'),
        ('Arms', 'Upper Body', 'Biceps and Triceps')
    ]
    cursor.executemany("INSERT INTO MuscleGroup (name, target_region, description) VALUES (?, ?, ?)", muscle_groups)

    # 2. Equipment (5 rows)
    equipment = [
        ('Barbell', 'Free Weight', 'Compound movements'),
        ('Dumbbell', 'Free Weight', 'Isolation and stability'),
        ('Cable Machine', 'Machine', 'Constant tension'),
        ('Leg Press', 'Machine', 'Lower body strength'),
        ('Pull-up Bar', 'Bodyweight', 'Upper body pulling')
    ]
    cursor.executemany("INSERT INTO Equipment (name, category, target_muscle_focus) VALUES (?, ?, ?)", equipment)

    # 3. WorkoutSession (6 rows)
    sessions = [
        ('2023-10-01', 5, 'Great pump, felt strong.', '/photos/oct1.jpg'),
        ('2023-10-03', 4, 'Tired but pushed through.', None),
        ('2023-10-05', 3, 'Lower back tightness.', '/photos/oct5.jpg'),
        ('2023-10-08', 5, 'PR on bench press!', '/photos/pr_bench.jpg'),
        ('2023-10-10', 4, 'Leg day, very sore.', None),
        ('2023-10-12', 5, 'High volume arm workout.', '/photos/arms.jpg')
    ]
    cursor.executemany(
        "INSERT INTO WorkoutSession (workout_date, session_rating, notes, photo_path) VALUES (?, ?, ?, ?)", sessions)

    # 4. Exercise (10 rows)
    # Note: muscle_group_id 1=Chest, 2=Back, 3=Legs, 4=Shoulders, 5=Arms
    exercises = [
        (1, 'Bench Press', 'Compound', 'Intermediate'),
        (1, 'Cable Fly', 'Isolation', 'Beginner'),
        (2, 'Deadlift', 'Compound', 'Advanced'),
        (2, 'Lat Pulldown', 'Compound', 'Beginner'),
        (3, 'Squat', 'Compound', 'Advanced'),
        (3, 'Leg Extension', 'Isolation', 'Beginner'),
        (4, 'Overhead Press', 'Compound', 'Intermediate'),
        (4, 'Lateral Raise', 'Isolation', 'Beginner'),
        (5, 'Bicep Curl', 'Isolation', 'Beginner'),
        (5, 'Tricep Pushdown', 'Isolation', 'Beginner')
    ]
    cursor.executemany(
        "INSERT INTO Exercise (muscle_group_id, name, mechanic_type, difficulty_level) VALUES (?, ?, ?, ?)", exercises)

    # 5. WorkoutExercise (15 rows)
    # Note: Links workout_id to exercise_id
    workout_exercises = [
        (1, 1, 4, 8, 135.0),  # Session 1: Bench Press
        (1, 2, 3, 12, 40.0),  # Session 1: Cable Fly
        (1, 9, 3, 15, 25.0),  # Session 1: Bicep Curl
        (2, 3, 3, 5, 225.0),  # Session 2: Deadlift
        (2, 4, 3, 10, 120.0),  # Session 2: Lat Pulldown
        (3, 5, 3, 10, 185.0),  # Session 3: Squat
        (3, 6, 3, 15, 90.0),  # Session 3: Leg Extension
        (4, 1, 5, 5, 155.0),  # Session 4: Bench Press (PR)
        (4, 7, 3, 8, 95.0),  # Session 4: Overhead Press
        (5, 5, 4, 8, 205.0),  # Session 5: Squat
        (5, 6, 4, 12, 100.0),  # Session 5: Leg Extension
        (5, 3, 3, 5, 245.0),  # Session 5: Deadlift
        (6, 9, 4, 12, 30.0),  # Session 6: Bicep Curl
        (6, 10, 4, 12, 50.0),  # Session 6: Tricep Pushdown
        (6, 8, 3, 15, 20.0)  # Session 6: Lateral Raise
    ]
    cursor.executemany(
        "INSERT INTO WorkoutExercise (workout_id, exercise_id, sets_completed, target_reps, weight_used) VALUES (?, ?, ?, ?, ?)",
        workout_exercises)

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print(f"Database '{DB_PATH}' created and populated successfully.")


if __name__ == "__main__":
    # Remove existing DB file to ensure a fresh start
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    create_database()