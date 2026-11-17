# Authors: Levi Ransom, Roger Major
# Date: 11/17/2026
# File: workout_exceptions.py
# Description: Define the workout session data access exception.

class WorkoutDataError(Exception):
    """Raised when workout session records cannot be loaded."""
