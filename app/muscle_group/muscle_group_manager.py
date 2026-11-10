from sqlalchemy.exc import SQLAlchemyError

from app.muscle_group.models import MuscleGroup
from app.muscle_group.muscle_group_exceptions import MuscleGroupDataError
from extensions import db


def get_all_muscle_groups():
    # Load all muscle groups for the list page.
    try:
        return MuscleGroup.query.all()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise MuscleGroupDataError("Muscle groups could not be loaded. Please try again later.") from error
